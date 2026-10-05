"""Serviço de extração de cor dominante."""

import logging
import math
from typing import Optional, Tuple

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def estimate_background(image: Image.Image) -> Tuple[int, int, int]:
    """Cor de fundo estimada: mediana dos pixels da borda da imagem."""
    img = np.array(image.convert("RGB").resize((100, 100))).astype(np.float64)
    border = np.concatenate([img[0, :], img[-1, :], img[:, 0], img[:, -1]])
    r, g, b = np.median(border, axis=0).astype(int)
    return int(r), int(g), int(b)


def extract_dominant_hex(
    image_crop: Image.Image,
    n_clusters: int = 3,
    background: Optional[Tuple[int, int, int]] = None,
) -> str:
    """Extrai a cor dominante de um crop de imagem usando KMeans.

    Args:
        image_crop: Imagem PIL já recortada.
        n_clusters: Número de clusters para KMeans.
        background: Cor de fundo da foto original. O cluster parecido com ela
            é descartado (se sobrar outro com pelo menos 15% dos pixels).

    Returns:
        Cor dominante em formato HEX (ex: "#202020").
    """
    # Com canal alfa (silhueta do YOLO-seg), só os pixels da pessoa entram na conta
    img = image_crop.convert("RGBA").resize((100, 100))
    rgba = np.array(img).reshape(-1, 4).astype(np.float64)
    pixels = rgba[rgba[:, 3] > 128][:, :3]
    if len(pixels) < 100:
        pixels = rgba[:, :3]

    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(pixels)

    # Clusters do maior para o menor; pula o que for fundo
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    order = labels[np.argsort(-counts)]
    shares = dict(zip(labels, counts / counts.sum()))
    dominant_idx = order[0]
    if background is not None:
        bg = np.array(background, dtype=np.float64)
        for idx in order:
            is_bg = np.linalg.norm(kmeans.cluster_centers_[idx] - bg) < 45
            if not is_bg and shares[idx] >= 0.15:
                dominant_idx = idx
                break
    dominant_color = kmeans.cluster_centers_[dominant_idx].astype(int)

    r, g, b = int(dominant_color[0]), int(dominant_color[1]), int(dominant_color[2])
    hex_color = rgb_to_hex(r, g, b)

    logger.info("Cor dominante extraída: %s (RGB: %d, %d, %d)", hex_color, r, g, b)
    return hex_color


def color_distance(hex1: str, hex2: str) -> float:
    """Distância euclidiana entre duas cores HEX no espaço RGB.

    Retorna valor entre 0 (idêntica) e ~441 (máxima distância).
    """
    r1, g1, b1 = hex_to_rgb(hex1)
    r2, g2, b2 = hex_to_rgb(hex2)
    return float(np.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2))


def hex_to_lab(hex_color: str) -> Tuple[float, float, float]:
    """HEX → CIELAB (iluminante D65), o espaço de cor feito para imitar a visão humana."""
    rgb = [c / 255.0 for c in hex_to_rgb(hex_color)]
    # sRGB → linear
    lin = [((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92 for c in rgb]
    x = (lin[0] * 0.4124 + lin[1] * 0.3576 + lin[2] * 0.1805) / 0.95047
    y = lin[0] * 0.2126 + lin[1] * 0.7152 + lin[2] * 0.0722
    z = (lin[0] * 0.0193 + lin[1] * 0.1192 + lin[2] * 0.9505) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def delta_e_2000(hex1: str, hex2: str) -> float:
    """Diferença de cor perceptual CIEDE2000 (0 = idêntica; ~2 = mal se nota; >20 = cores diferentes).

    Ao contrário da distância RGB, dá mais peso à diferença de matiz (tom):
    um rosa acinzentado fica mais perto de um rosa claro do que de um bege.
    """
    L1, a1, b1 = hex_to_lab(hex1)
    L2, a2, b2 = hex_to_lab(hex2)

    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    C_bar = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(C_bar ** 7 / (C_bar ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360

    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))

    L_bar = (L1 + L2) / 2
    Cp_bar = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hp_bar = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hp_bar = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hp_bar = (h1p + h2p + 360) / 2
    else:
        hp_bar = (h1p + h2p - 360) / 2

    T = (1 - 0.17 * math.cos(math.radians(hp_bar - 30))
         + 0.24 * math.cos(math.radians(2 * hp_bar))
         + 0.32 * math.cos(math.radians(3 * hp_bar + 6))
         - 0.20 * math.cos(math.radians(4 * hp_bar - 63)))
    S_L = 1 + 0.015 * (L_bar - 50) ** 2 / math.sqrt(20 + (L_bar - 50) ** 2)
    S_C = 1 + 0.045 * Cp_bar
    S_H = 1 + 0.015 * Cp_bar * T
    R_T = (-2 * math.sqrt(Cp_bar ** 7 / (Cp_bar ** 7 + 25 ** 7))
           * math.sin(math.radians(60 * math.exp(-((hp_bar - 275) / 25) ** 2))))

    return math.sqrt(
        (dLp / S_L) ** 2 + (dCp / S_C) ** 2 + (dHp / S_H) ** 2
        + R_T * (dCp / S_C) * (dHp / S_H)
    )


# ΔE a partir do qual a similaridade de cor é zero
DELTA_E_MAX = 50.0

# Abaixo deste croma (C* em LCh) a cor é considerada neutra: branco, cinza, preto
CHROMA_NEUTRO = 5.0

# Peso do matiz na similaridade de cor (o resto vai para o ΔE2000)
PESO_MATIZ = 0.6


def hue_similarity(hex1: str, hex2: str) -> float:
    """Similaridade de matiz (tom) entre 0 e 1, no espaço LCh.

    É como as pessoas dão nome às cores: um rosa bem claro e um rosa forte têm o
    mesmo matiz, embora fiquem longe no ΔE. Cores neutras não têm matiz, então:
    - duas neutras → comparadas pela luminosidade;
    - uma neutra e uma colorida → similaridade baixa (0,3).
    """
    L1, a1, b1 = hex_to_lab(hex1)
    L2, a2, b2 = hex_to_lab(hex2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    neutra1, neutra2 = C1 < CHROMA_NEUTRO, C2 < CHROMA_NEUTRO
    if neutra1 and neutra2:
        return 1.0 - abs(L1 - L2) / 100.0
    if neutra1 or neutra2:
        return 0.3
    h1 = math.degrees(math.atan2(b1, a1)) % 360
    h2 = math.degrees(math.atan2(b2, a2)) % 360
    dh = abs(h1 - h2)
    dh = min(dh, 360 - dh)  # o círculo de matiz dá a volta: 350° fica perto de 10°
    return 1.0 - dh / 180.0


def color_similarity(hex1: str, hex2: str) -> float:
    """Similaridade de cor entre 0 e 1.

    sim_cor = 0,6 × sim_matiz + 0,4 × (1 − ΔE2000 / 50)
    O matiz decide "que cor é" (rosa, azul, verde...); o ΔE2000 refina por
    claridade e saturação.
    """
    sim_de = max(0.0, 1.0 - delta_e_2000(hex1, hex2) / DELTA_E_MAX)
    return PESO_MATIZ * hue_similarity(hex1, hex2) + (1 - PESO_MATIZ) * sim_de
