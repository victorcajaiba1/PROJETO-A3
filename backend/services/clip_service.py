"""Serviço de embeddings visuais usando CLIP."""

import logging
from typing import Dict, List, Optional

import numpy as np
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

logger = logging.getLogger(__name__)


class ClipService:
    """Gera embeddings visuais com CLIP para busca por similaridade."""

    def __init__(self) -> None:
        self._model: Optional[CLIPModel] = None
        self._processor: Optional[CLIPProcessor] = None
        self._device: str = "cuda" if torch.cuda.is_available() else "cpu"

    def _load_model(self) -> None:
        if self._model is None:
            model_name = "openai/clip-vit-base-patch32"
            logger.info("Carregando CLIP (%s) no device=%s...", model_name, self._device)
            self._processor = CLIPProcessor.from_pretrained(model_name)
            self._model = CLIPModel.from_pretrained(model_name).to(self._device)
            self._model.eval()
            logger.info("CLIP carregado com sucesso.")

    def encode_image(self, image: Image.Image) -> List[float]:
        """Gera embedding de uma imagem PIL.

        Returns:
            Lista de floats representando o embedding normalizado.
        """
        self._load_model()
        inputs = self._processor(images=image, return_tensors="pt").to(self._device)

        with torch.no_grad():
            features = self._model.get_image_features(**inputs)

        # Normalizar para similaridade cosseno
        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features.squeeze().cpu().tolist()

    def encode_text(self, text: str) -> List[float]:
        """Gera embedding de um texto usando CLIP.

        Útil como fallback para produtos sem imagem, já que CLIP compartilha
        o mesmo espaço de embeddings entre texto e imagem.

        Returns:
            Lista de floats representando o embedding normalizado.
        """
        self._load_model()
        inputs = self._processor(text=[text], return_tensors="pt", padding=True, truncation=True).to(self._device)

        with torch.no_grad():
            features = self._model.get_text_features(**inputs)

        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features.squeeze().cpu().tolist()

    def classify(self, image: Image.Image, labels: Dict[str, str]) -> str:
        """Classificação zero-shot: escolhe a descrição textual mais parecida com a imagem.

        Args:
            image: Imagem PIL.
            labels: Mapa {chave: descrição em inglês}, ex.: {"shorts": "a photo of shorts"}.

        Returns:
            A chave com maior probabilidade.
        """
        self._load_model()
        keys = list(labels.keys())
        inputs = self._processor(
            text=[labels[k] for k in keys], images=image, return_tensors="pt", padding=True
        ).to(self._device)

        with torch.no_grad():
            probs = self._model(**inputs).logits_per_image.softmax(dim=-1).squeeze(0)

        best = int(probs.argmax())
        logger.info(
            "CLIP zero-shot: %s",
            ", ".join("{}={:.2f}".format(k, float(p)) for k, p in zip(keys, probs)),
        )
        return keys[best]

    def cosine_similarity(self, embedding_a: List[float], embedding_b: List[float]) -> float:
        """Calcula similaridade cosseno entre dois embeddings."""
        a = np.array(embedding_a)
        b = np.array(embedding_b)
        dot = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot / (norm_a * norm_b))


# Singleton
clip_service = ClipService()
