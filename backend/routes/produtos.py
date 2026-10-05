"""Rotas do catálogo: o PostgreSQL é a fonte oficial dos produtos do site.

As respostas usam o mesmo formato do catálogo em js/produtos.js
(categoria e esporte como slug, tamanhos em lista, imagem principal).
"""

import logging
from contextlib import contextmanager
from decimal import Decimal
from typing import List, Literal, Optional

import psycopg
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.auth import exigir_admin
from backend.db import banco_configurado, conectar

logger = logging.getLogger(__name__)
router = APIRouter()

ORDEM_TAMANHOS = ["PP", "P", "M", "G", "GG", "XG"]
PREFIXO_SKU = {"camisetas": "CAM", "calcas": "CAL", "jaquetas": "JAQ", "moletons": "MOL", "shorts": "SHO"}

SELECT_PRODUTOS = """
    SELECT p.id, p.nome, COALESCE(p.descricao, ''), p.preco, c.slug,
           COALESCE(m.slug, ''), COALESCE(p.cor_nome, ''), COALESCE(p.cor_hex, '#808080'),
           p.estoque,
           COALESCE((SELECT i.url FROM imagens_produto i
                     WHERE i.produto_id = p.id AND i.principal LIMIT 1), ''),
           COALESCE((SELECT array_agg(t.tamanho) FROM produto_tamanhos t
                     WHERE t.produto_id = p.id), '{}')
    FROM produtos p
    JOIN categorias c ON c.id = p.categoria_id
    LEFT JOIN modalidades m ON m.id = p.modalidade_id
    WHERE p.ativo
"""


class ProdutoIn(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    descricao: str = Field(default="", max_length=2000)
    preco: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    categoria: str
    esporte: str = ""
    tamanhos: List[Literal["PP", "P", "M", "G", "GG", "XG"]] = Field(default_factory=lambda: ["P", "M", "G"])
    cor: str = Field(default="", max_length=40)
    hex_color: str = Field(default="#808080", pattern=r"^#[0-9a-fA-F]{6}$")
    imagem: str = Field(default="", max_length=3_000_000)  # caminho, URL ou data URL
    estoque: int = Field(ge=0)


def _linha_para_produto(row) -> dict:
    (pid, nome, descricao, preco, categoria, esporte, cor, hex_color,
     estoque, imagem, tamanhos) = row
    return {
        "id": pid,
        "nome": nome,
        "descricao": descricao,
        "preco": float(preco),
        "categoria": categoria,
        "tamanhos": sorted(tamanhos, key=ORDEM_TAMANHOS.index),
        "cor": cor,
        "hex_color": hex_color,
        "imagem": imagem,
        "estoque": estoque,
        "esporte": esporte,
    }


@contextmanager
def _conexao():
    """Abre a transação e traduz falhas do banco em respostas HTTP."""
    if not banco_configurado():
        raise HTTPException(status_code=503, detail="Banco de dados não configurado.")
    try:
        with conectar() as conn, conn.cursor() as cur:
            yield cur
    except (psycopg.errors.IntegrityError, psycopg.errors.DataError) as e:
        logger.warning("Produto rejeitado pelo banco: %s", e)
        raise HTTPException(status_code=422, detail="Dados do produto inválidos.")
    except psycopg.OperationalError as e:
        logger.error("Banco indisponível: %s", e)
        raise HTTPException(status_code=503, detail="Banco de dados indisponível.")


def _buscar(cur: psycopg.Cursor, produto_id: int) -> dict:
    cur.execute(SELECT_PRODUTOS + " AND p.id = %s", (produto_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return _linha_para_produto(row)


def _ids_de_classificacao(cur: psycopg.Cursor, dados: ProdutoIn):
    cur.execute("SELECT id FROM categorias WHERE slug = %s AND ativo", (dados.categoria,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=422, detail=f"Categoria inválida: {dados.categoria}")
    categoria_id = row[0]
    modalidade_id: Optional[int] = None
    if dados.esporte:
        cur.execute("SELECT id FROM modalidades WHERE slug = %s AND ativo", (dados.esporte,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=422, detail=f"Esporte inválido: {dados.esporte}")
        modalidade_id = row[0]
    return categoria_id, modalidade_id


def _gravar_detalhes(cur: psycopg.Cursor, produto_id: int, dados: ProdutoIn) -> None:
    """Substitui tamanhos e foto principal pelos enviados pelo admin."""
    cur.execute("DELETE FROM produto_tamanhos WHERE produto_id = %s", (produto_id,))
    for tamanho in dict.fromkeys(dados.tamanhos):
        cur.execute("INSERT INTO produto_tamanhos (produto_id, tamanho) VALUES (%s, %s)",
                    (produto_id, tamanho))

    cur.execute("SELECT id, url FROM imagens_produto WHERE produto_id = %s AND principal",
                (produto_id,))
    atual = cur.fetchone()
    if atual and atual[1] == dados.imagem:
        return
    if atual:
        # Processamento de IA da foto antiga sai junto (ON DELETE CASCADE)
        cur.execute("DELETE FROM imagens_produto WHERE id = %s", (atual[0],))
    if dados.imagem:
        cur.execute(
            "INSERT INTO imagens_produto (produto_id, url, ordem, principal) VALUES (%s, %s, 0, true)",
            (produto_id, dados.imagem),
        )


@router.get("/produtos")
def listar_produtos():
    with _conexao() as cur:
        cur.execute(SELECT_PRODUTOS + " ORDER BY p.id")
        return [_linha_para_produto(row) for row in cur.fetchall()]


@router.post("/produtos", status_code=201, dependencies=[Depends(exigir_admin)])
def criar_produto(dados: ProdutoIn):
    with _conexao() as cur:
        categoria_id, modalidade_id = _ids_de_classificacao(cur, dados)
        # SKU definitivo depende do id: grava um provisório e troca em seguida
        cur.execute(
            """INSERT INTO produtos (sku, nome, descricao, categoria_id, modalidade_id,
                                     preco, estoque, cor_nome, cor_hex)
               VALUES ('NOVO-' || substr(md5(random()::text), 1, 16), %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (dados.nome, dados.descricao, categoria_id, modalidade_id, dados.preco,
             dados.estoque, dados.cor or None, dados.hex_color),
        )
        produto_id = cur.fetchone()[0]
        prefixo = PREFIXO_SKU.get(dados.categoria, "PRD")
        cur.execute("UPDATE produtos SET sku = %s WHERE id = %s",
                    (f"{prefixo}-{produto_id:04d}", produto_id))
        _gravar_detalhes(cur, produto_id, dados)
        produto = _buscar(cur, produto_id)
    logger.info("Produto %s criado", produto_id)
    return produto


@router.put("/produtos/{produto_id}", dependencies=[Depends(exigir_admin)])
def editar_produto(produto_id: int, dados: ProdutoIn):
    with _conexao() as cur:
        categoria_id, modalidade_id = _ids_de_classificacao(cur, dados)
        cur.execute(
            """UPDATE produtos
               SET nome = %s, descricao = %s, categoria_id = %s, modalidade_id = %s,
                   preco = %s, estoque = %s, cor_nome = %s, cor_hex = %s
               WHERE id = %s AND ativo""",
            (dados.nome, dados.descricao, categoria_id, modalidade_id, dados.preco,
             dados.estoque, dados.cor or None, dados.hex_color, produto_id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")
        _gravar_detalhes(cur, produto_id, dados)
        produto = _buscar(cur, produto_id)
    logger.info("Produto %s atualizado", produto_id)
    return produto


@router.delete("/produtos/{produto_id}", status_code=204, dependencies=[Depends(exigir_admin)])
def remover_produto(produto_id: int):
    """Exclusão lógica: pedidos antigos continuam apontando para o produto."""
    with _conexao() as cur:
        cur.execute("UPDATE produtos SET ativo = false WHERE id = %s AND ativo", (produto_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")
    logger.info("Produto %s desativado", produto_id)
