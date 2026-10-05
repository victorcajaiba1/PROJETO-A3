"""Serviço de recomendação: combina CLIP + cor para ranking híbrido."""

import base64
import hashlib
import logging
import urllib.request
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image

from backend.models.product import SearchResult
from backend.services.clip_service import clip_service
from backend.services.color_service import color_similarity, estimate_background, extract_dominant_hex
from backend.services.yolo_service import yolo_service

logger = logging.getLogger(__name__)

# Catálogo indexado (com embeddings) fica só em memória: o frontend reenvia o
# catálogo antes de cada busca. Gravar em disco dentro do projeto fazia o
# Live Server do VS Code recarregar a página no meio da busca.
_catalog: List[Dict[str, Any]] = []

# Raiz do frontend: imagens de produto com caminho relativo (ex.: img/produtos/x.jpg)
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent

# Cache de embeddings por imagem: o frontend reenvia o catálogo a cada busca,
# então só as imagens novas ou alteradas passam pelo YOLO + CLIP.
_embedding_cache: Dict[str, List[float]] = {}


def _name_to_hex(color_name: str) -> str:
    """Mapeia nomes de cor do catálogo para HEX aproximado."""
    mapping = {
        "preto": "#1a1a1a",
        "branco": "#f5f5f5",
        "cinza": "#808080",
        "azul marinho": "#1b2a4a",
        "verde militar": "#4b5320",
        "vermelho": "#c0392b",
        "azul": "#2980b9",
        "rosa": "#e91e8c",
        "amarelo": "#f1c40f",
        "laranja": "#e67e22",
        "bege": "#d4c5a9",
        "marrom": "#6b4226",
    }
    return mapping.get(color_name.lower().strip(), "#808080")


# Categorias do catálogo (mesmas chaves do frontend) e descrições para o CLIP zero-shot
CATEGORY_PROMPTS = {
    "camisetas": "a photo of a t-shirt or sports jersey",
    "calcas": "a photo of long pants or leggings",
    "jaquetas": "a photo of a jacket or windbreaker",
    "moletons": "a photo of a hoodie or sweatshirt",
    "shorts": "a photo of shorts",
}

# Faixa vertical (em fração da altura da pessoa) onde cada peça costuma ficar
BODY_REGIONS = {
    "camisetas": (0.15, 0.55),
    "jaquetas": (0.15, 0.60),
    "moletons": (0.15, 0.60),
    "shorts": (0.45, 0.70),
    "calcas": (0.45, 0.95),
}


def _crop_garment(person: Image.Image, category: str) -> Image.Image:
    """Recorta, no corpo da pessoa, a região onde está a peça detectada."""
    top, bottom = BODY_REGIONS.get(category, (0.15, 0.65))
    w, h = person.size
    # Margem lateral de 20% para tirar braços e fundo da cor dominante
    return person.crop((int(w * 0.2), int(h * top), int(w * 0.8), int(h * bottom)))


def extract_garment(image: Image.Image, category: Optional[str] = None) -> Tuple[Image.Image, str]:
    """Mesmo recorte para a foto do usuário e para as fotos do catálogo.

    YOLO acha a pessoa, o CLIP diz qual peça é (se a categoria não for conhecida)
    e o recorte fica só na região do corpo onde a peça está.
    """
    crop, yolo_label = yolo_service.detect_and_crop(image)
    if not category:
        category = clip_service.classify(to_rgb(crop), CATEGORY_PROMPTS)
    if yolo_label == "pessoa":
        crop = _crop_garment(crop, category)
    return crop, category


def to_rgb(crop: Image.Image) -> Image.Image:
    """Recorte com fundo transparente → RGB sobre cinza neutro (entrada do CLIP)."""
    if crop.mode != "RGBA":
        return crop.convert("RGB")
    base = Image.new("RGB", crop.size, (128, 128, 128))
    base.paste(crop, mask=crop.split()[3])
    return base


def _load_product_image(src: str) -> Optional[Image.Image]:
    """Abre a imagem do produto: data URI/base64, URL http(s) ou caminho do frontend."""
    if src.startswith("http://") or src.startswith("https://"):
        req = urllib.request.Request(src, headers={"User-Agent": "TechWear/1.0"})
        data = urllib.request.urlopen(req, timeout=10).read()
    elif src.startswith("data:") or len(src) > 300:
        data = base64.b64decode(src.split(",")[-1])
    else:
        path = (FRONTEND_DIR / src.lstrip("/")).resolve()
        if not path.is_relative_to(FRONTEND_DIR) or not path.is_file():
            return None
        data = path.read_bytes()
    return Image.open(BytesIO(data)).convert("RGB")


def load_catalog() -> List[Dict[str, Any]]:
    """Catálogo de produtos com embeddings (último enviado pelo frontend)."""
    return _catalog


def save_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Guarda o catálogo indexado em memória."""
    global _catalog
    _catalog = catalog
    logger.info("Catálogo indexado com %d produtos", len(catalog))


def index_products_from_frontend(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Indexa produtos do frontend (localStorage) gerando embeddings e hex_color.

    Recebe a lista de produtos no formato do TechWear JS e retorna
    o catálogo indexado com embeddings CLIP.
    """
    catalog: List[Dict[str, Any]] = []

    for p in products:
        # Preferir hex_color já definido no produto (via color picker do admin)
        # e usar _name_to_hex apenas como fallback para cores sem HEX
        hex_color = p.get("hex_color") or _name_to_hex(p.get("cor", ""))

        entry = {
            "id": p["id"],
            "name": p.get("nome", ""),
            "hex_color": hex_color,
            "category": p.get("categoria", ""),
            "price": p.get("preco", 0),
            "image_url": p.get("imagem", ""),
            "embedding": [],  # Será preenchido quando houver imagem
        }

        # Com imagem: embedding visual do recorte da peça (mesmo pipeline da busca)
        image_src = p.get("imagem", "") or ""
        if image_src:
            cache_key = hashlib.sha1(
                (image_src + "|" + entry["category"]).encode("utf-8")
            ).hexdigest()
            try:
                if cache_key not in _embedding_cache:
                    img = _load_product_image(image_src)
                    if img is None:
                        raise ValueError("imagem não encontrada: " + image_src[:80])
                    crop, _ = extract_garment(img, entry["category"] or None)
                    _embedding_cache[cache_key] = clip_service.encode_image(to_rgb(crop))
                    logger.info("Embedding de imagem gerado para produto %s: %s", p["id"], p.get("nome"))
                entry["embedding"] = _embedding_cache[cache_key]
            except Exception as e:
                logger.warning("Erro ao gerar embedding de imagem do produto %s: %s", p["id"], e)

        if not entry["embedding"]:
            # Fallback: usar embedding de texto quando não há imagem.
            # CLIP compartilha o mesmo espaço vetorial entre imagem e texto,
            # permitindo comparar a query visual com a descrição textual do produto.
            try:
                text = "{} {} {} {}".format(
                    p.get("nome", ""),
                    p.get("cor", ""),
                    p.get("categoria", ""),
                    p.get("esporte", ""),
                ).strip()
                entry["embedding"] = clip_service.encode_text(text)
                logger.info("Embedding de texto gerado para produto %s: %s", p["id"], p.get("nome"))
            except Exception as e:
                logger.warning("Erro ao gerar embedding de texto do produto %s: %s", p["id"], e)

        catalog.append(entry)

    save_catalog(catalog)
    return catalog


def search_by_image(
    image: Image.Image,
    category: Optional[str] = None,
    top_k: int = 5,
    clip_weight: float = 0.7,
    color_weight: float = 0.3,
) -> Dict[str, Any]:
    """Fluxo principal: imagem → YOLO → cor + CLIP → ranking.

    Args:
        image: Imagem PIL enviada pelo usuário.
        category: Tipo de peça já conhecido (filtro do usuário); None = detectar.
        top_k: Quantidade de resultados.
        clip_weight: Peso da similaridade visual (CLIP).
        color_weight: Peso da similaridade de cor (matiz + ΔE2000).

    Returns:
        Dict com detected_hex, detected_category e lista de produtos rankeados.
    """
    # 1. YOLO (pessoa) + CLIP zero-shot (tipo de peça) + recorte da região da peça
    if category not in CATEGORY_PROMPTS:
        category = None
    crop, detected_category = extract_garment(image, category)
    logger.info("Peça detectada: categoria=%s", detected_category)

    # 2. Extrair cor dominante do crop
    detected_hex = extract_dominant_hex(crop, background=estimate_background(image))
    logger.info("Cor detectada: %s", detected_hex)

    # 3. Gerar embedding CLIP do crop
    query_embedding = clip_service.encode_image(to_rgb(crop))

    # 4. Carregar catálogo
    catalog = load_catalog()
    if not catalog:
        logger.warning("Catálogo vazio. Retornando resultado vazio.")
        return {
            "detected_hex": detected_hex,
            "detected_category": detected_category,
            "products": [],
        }

    # 5. Calcular scores híbridos
    scored: List[Dict[str, Any]] = []
    for product in catalog:
        prod_embedding = product.get("embedding", [])

        # Similaridade CLIP (visual)
        if prod_embedding and query_embedding:
            clip_sim = clip_service.cosine_similarity(query_embedding, prod_embedding)
        else:
            clip_sim = 0.0

        # Similaridade de cor
        prod_hex = product.get("hex_color", "#808080")
        color_sim = color_similarity(detected_hex, prod_hex)

        final_score = clip_weight * clip_sim + color_weight * color_sim

        scored.append(
            {
                "id": product["id"],
                "name": product["name"],
                "hex_color": product.get("hex_color", ""),
                "category": product.get("category", ""),
                "price": product.get("price", 0),
                "image_url": product.get("image_url", ""),
                "score": round(final_score, 4),
            }
        )

    # 6. Ordenar por score (para restringir o tipo de peça, o usuário usa o filtro)
    scored.sort(key=lambda x: x["score"], reverse=True)
    top_results = scored[:top_k]

    logger.info(
        "Busca concluída. Top %d resultados retornados (melhor score=%.4f)",
        len(top_results),
        top_results[0]["score"] if top_results else 0,
    )

    return {
        "detected_hex": detected_hex,
        "detected_category": detected_category,
        "products": [SearchResult(**r) for r in top_results],
    }
