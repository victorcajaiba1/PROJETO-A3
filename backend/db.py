"""Conexão com o PostgreSQL (Railway injeta DATABASE_URL pela rede privada)."""

import logging
import os
from pathlib import Path

import psycopg

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "")

# Scripts idempotentes reaplicados a cada boot. O seed (03) fica de fora:
# reexecutá-lo devolveria tamanhos e fotos que o admin removeu.
SCRIPTS_SCHEMA = ["01_schema.sql", "02_procedures.sql"]
DATABASE_DIR = Path(__file__).resolve().parent.parent / "database"


def banco_configurado() -> bool:
    return bool(DATABASE_URL)


def conectar() -> psycopg.Connection:
    """Abre uma conexão nova. O volume de acessos não justifica um pool."""
    return psycopg.connect(DATABASE_URL, connect_timeout=5)


def aplicar_schema() -> None:
    """Mantém tabelas e procedures do banco iguais aos arquivos em database/."""
    if not banco_configurado():
        logger.warning("DATABASE_URL não definida: catálogo e pedidos ficam só no navegador.")
        return
    try:
        # autocommit: os scripts trazem o próprio BEGIN/COMMIT
        with psycopg.connect(DATABASE_URL, connect_timeout=5, autocommit=True) as conn:
            for nome in SCRIPTS_SCHEMA:
                conn.execute((DATABASE_DIR / nome).read_text(encoding="utf-8"))
        logger.info("Schema do banco atualizado.")
    except Exception as e:
        # O site continua no ar; as rotas do banco respondem 503
        logger.error("Falha ao aplicar o schema do banco: %s", e)
