# Tech Wear — imagem única (frontend + API WearIA)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/models/huggingface \
    YOLO_CONFIG_DIR=/opt/models/ultralytics \
    YOLO_AUTOINSTALL=False

# Bibliotecas de sistema exigidas pelo OpenCV (dependência do Ultralytics)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Tudo num único pip install: o PyTorch versão CPU (a do PyPI traz CUDA e passa
# de 2 GB) vem do índice extra, e o numpy 2.x nunca chega a ser instalado.
# Instalar o torch numa camada e trocar o numpy em outra deixava arquivos do
# numpy 2.x no container e quebrava o boot ("numpy._core.multiarray failed").
COPY backend/requirements.txt backend/requirements.txt
RUN pip install torch==2.4.1+cpu torchvision==0.19.1+cpu -r backend/requirements.txt \
        --extra-index-url https://download.pytorch.org/whl/cpu \
    && python -c "import numpy, scipy.sparse, sklearn.cluster, cv2, torch, transformers, ultralytics; \
assert numpy.__version__ == '1.26.4', numpy.__version__"

# Baixa os modelos no build para a primeira busca não esperar o download
RUN mkdir -p /opt/models/yolo \
    && cd /opt/models/yolo \
    && python -c "from ultralytics import YOLO; YOLO('yolov8n-seg.pt')" \
    && python -c "from transformers import CLIPModel, CLIPProcessor; \
m='openai/clip-vit-base-patch32'; CLIPProcessor.from_pretrained(m); CLIPModel.from_pretrained(m)"

COPY . .
RUN ln -sf /opt/models/yolo/yolov8n-seg.pt /app/yolov8n-seg.pt \
    && python -c "import backend.main"

EXPOSE 8000
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
