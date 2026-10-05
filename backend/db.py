"""Conexão com o PostgreSQL (Railway injeta DATABASE_URL pela rede privada)."""

import os

import psycopg

DATABASE_URL = os.getenv("DATABASE_URL", "")


def banco_configurado() -> bool:
    return bool(DATABASE_URL)


def conectar() -> psycopg.Connection:
    """Abre uma conexão nova. O volume de pedidos não justifica um pool."""
    return psycopg.connect(DATABASE_URL, connect_timeout=5)
