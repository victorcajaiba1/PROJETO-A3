"""Tech Wear — servidor único (API FastAPI + frontend estático)."""

import logging
import os
from pathlib import Path

import pillow_heif
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.routes.image_search import router as image_router

# Registra o plugin AVIF/HEIC no Pillow. Sem isso, Image.open() rejeita fotos
# .avif/.heic (comuns em downloads do Unsplash e fotos de iPhone) com
# "cannot identify image file".
pillow_heif.register_heif_opener()
pillow_heif.register_avif_opener()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Raiz do projeto: onde ficam os .html, css/, js/ e imagens
FRONTEND_DIR = Path(__file__).resolve().parent.parent

# Apenas estes tipos de arquivo são servidos ao navegador.
# Impede que código do backend, .git, documentos etc. fiquem públicos.
ALLOWED_EXTENSIONS = {
    ".html", ".css", ".js", ".json", ".map",
    ".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg", ".ico",
    ".woff", ".woff2", ".ttf",
}
BLOCKED_DIRS = {"backend", ".git", ".venv", "venv", "node_modules"}

app = FastAPI(
    title="Tech Wear — WearIA API",
    description="Busca visual de roupas esportivas com YOLO + CLIP + cor HEX",
    version="1.0.0",
)

# CORS — útil quando o frontend é aberto por outro endereço (ex.: file://)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas da API
app.include_router(image_router, prefix="/api", tags=["Busca Visual"])


@app.get("/api/health")
async def health():
    return {"status": "online", "service": "Tech Wear WearIA API"}


# "no-cache": o navegador revalida a cada acesso, então um deploy novo
# nunca fica preso atrás de um JS/CSS antigo em cache.
NO_CACHE = {"Cache-Control": "no-cache"}


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(FRONTEND_DIR / "index.html", headers=NO_CACHE)


@app.get("/{file_path:path}", include_in_schema=False)
async def frontend(file_path: str):
    """Serve os arquivos do frontend (HTML, CSS, JS e imagens)."""
    target = (FRONTEND_DIR / file_path).resolve()

    parts = Path(file_path).parts
    if (
        not target.is_relative_to(FRONTEND_DIR)
        or not parts
        or parts[0] in BLOCKED_DIRS
        or any(p.startswith(".") for p in parts)
        or target.suffix.lower() not in ALLOWED_EXTENSIONS
        or not target.is_file()
    ):
        raise HTTPException(status_code=404, detail="Não encontrado.")

    return FileResponse(target, headers=NO_CACHE)
