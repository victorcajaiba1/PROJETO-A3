#!/usr/bin/env sh
# ========================================
# Tech Wear — sobe frontend + API WearIA num único servidor
# Uso (na raiz do projeto): sh backend/run.sh
# ========================================
set -e
cd "$(dirname "$0")/.."

# 1. Cria o ambiente virtual na primeira execução
if [ ! -d .venv ]; then
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r backend/requirements.txt
fi

# 2. Sobe o servidor
# Site:          http://localhost:8000
# Docs da API:   http://localhost:8000/docs
.venv/bin/uvicorn backend.main:app --reload --host 0.0.0.0 --port "${PORT:-8000}"
