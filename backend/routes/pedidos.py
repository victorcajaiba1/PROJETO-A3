"""Rotas de pedidos: grava a compra do checkout no PostgreSQL."""

import logging
from decimal import ROUND_HALF_UP, Decimal
from typing import List, Literal, Optional

import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.db import banco_configurado, conectar

logger = logging.getLogger(__name__)
router = APIRouter()

# Pedidos sem login ficam na conta de visitante (pedidos.cliente_id é obrigatório)
VISITANTE_EMAIL = "visitante@techwear.local"
# Senha bloqueada: o login ainda é feito no navegador, o servidor não guarda senha
SENHA_BLOQUEADA = "!"
# Mesma regra de pagamento.html: até 6x sem juros, acima disso 1,99% a.m. (Tabela Price)
TAXA_JUROS_MENSAL = Decimal("0.0199")
PARCELAS_SEM_JUROS = 6
CENTAVO = Decimal("0.01")


class UsuarioIn(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    email: str = Field(min_length=3, max_length=254)
    perfil: Literal["admin", "cliente"] = "cliente"


class ItemIn(BaseModel):
    produto_id: int
    tamanho: Literal["PP", "P", "M", "G", "GG", "XG"]
    quantidade: int = Field(gt=0, le=99)


class EntregaIn(BaseModel):
    destinatario: str = Field(min_length=1, max_length=150)
    cep: str
    logradouro: str = ""
    numero: str = Field(min_length=1, max_length=20)
    bairro: str = ""
    cidade: str = Field(min_length=1, max_length=100)
    estado: str = Field(min_length=2, max_length=2)
    tipo: Literal["padrao", "expressa"] = "padrao"
    valor_frete: Decimal = Field(ge=0)


class PagamentoIn(BaseModel):
    metodo: Literal["credito", "debito", "pix", "boleto"]
    parcelas: int = Field(default=1, ge=1, le=12)


class PedidoIn(BaseModel):
    usuario: Optional[UsuarioIn] = None
    itens: List[ItemIn] = Field(min_length=1)
    entrega: EntregaIn
    pagamento: PagamentoIn
    cupom: Optional[str] = None


class PedidoOut(BaseModel):
    pedido_id: int
    status: str
    subtotal: Decimal
    desconto: Decimal
    valor_frete: Decimal
    juros: Decimal
    total: Decimal


def _juros(base: Decimal, parcelas: int) -> Decimal:
    if parcelas <= PARCELAS_SEM_JUROS:
        return Decimal("0")
    r = TAXA_JUROS_MENSAL
    fator = (1 + r) ** parcelas
    parcela = base * (r * fator) / (fator - 1)
    return (parcela * parcelas - base).quantize(CENTAVO, ROUND_HALF_UP)


def _usuario_id(cur: psycopg.Cursor, usuario: Optional[UsuarioIn]) -> int:
    nome, email, perfil = (
        (usuario.nome, usuario.email.strip().lower(), usuario.perfil)
        if usuario else ("Visitante", VISITANTE_EMAIL, "cliente")
    )
    cur.execute(
        """INSERT INTO usuarios (nome, email, senha_hash) VALUES (%s, %s, %s)
           ON CONFLICT (email) DO UPDATE SET nome = EXCLUDED.nome
           RETURNING id""",
        (nome, email, SENHA_BLOQUEADA),
    )
    usuario_id = cur.fetchone()[0]
    cur.execute(
        """INSERT INTO usuario_papeis (usuario_id, papel_id)
           SELECT %s, id FROM papeis WHERE nome = %s
           ON CONFLICT DO NOTHING""",
        (usuario_id, perfil),
    )
    return usuario_id


@router.post("/pedidos", response_model=PedidoOut, status_code=201)
def criar_pedido(pedido: PedidoIn):
    """Registra pedido, itens, pagamento e entrega numa única transação.

    Preços vêm do banco, nunca do navegador. reservar_estoque impede saldo
    negativo em compras simultâneas; qualquer erro desfaz tudo (ROLLBACK).
    """
    if not banco_configurado():
        raise HTTPException(status_code=503, detail="Banco de dados não configurado.")

    entrega = pedido.entrega
    cep = "".join(c for c in entrega.cep if c.isdigit())
    if len(cep) != 8:
        raise HTTPException(status_code=422, detail="CEP inválido.")
    if pedido.pagamento.metodo != "credito" and pedido.pagamento.parcelas != 1:
        raise HTTPException(status_code=422, detail="Parcelamento só no cartão de crédito.")

    try:
        with conectar() as conn, conn.cursor() as cur:
            cliente_id = _usuario_id(cur, pedido.usuario)

            cupom_id, percentual = None, Decimal("0")
            if pedido.cupom:
                cur.execute(
                    """SELECT id, percentual FROM cupons
                       WHERE codigo = %s AND ativo
                         AND valido_de <= now() AND (valido_ate IS NULL OR valido_ate > now())""",
                    (pedido.cupom.strip().upper(),),
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=422, detail="Cupom inválido ou expirado.")
                cupom_id, percentual = row

            # Carrinho antigo que tenha ficado aberto é substituído por este pedido
            cur.execute(
                "UPDATE pedidos SET status = 'cancelado', cancelado_em = now() "
                "WHERE cliente_id = %s AND status = 'aberto'",
                (cliente_id,),
            )
            cur.execute(
                "INSERT INTO pedidos (cliente_id, cupom_id) VALUES (%s, %s) RETURNING id",
                (cliente_id, cupom_id),
            )
            pedido_id = cur.fetchone()[0]

            for item in pedido.itens:
                cur.execute("CALL reservar_estoque(%s, %s)", (item.produto_id, item.quantidade))
                cur.execute(
                    """INSERT INTO itens_pedido (pedido_id, produto_id, tamanho, quantidade, preco_unitario)
                       SELECT %s, id, %s, %s, preco FROM produtos WHERE id = %s
                       ON CONFLICT (pedido_id, produto_id, tamanho)
                       DO UPDATE SET quantidade = itens_pedido.quantidade + EXCLUDED.quantidade""",
                    (pedido_id, item.tamanho, item.quantidade, item.produto_id),
                )

            # O trigger tg_itens_subtotal já somou os itens
            cur.execute("SELECT subtotal FROM pedidos WHERE id = %s", (pedido_id,))
            subtotal = cur.fetchone()[0]
            desconto = (subtotal * percentual).quantize(CENTAVO, ROUND_HALF_UP)
            valor_frete = entrega.valor_frete.quantize(CENTAVO, ROUND_HALF_UP)
            juros = (
                _juros(subtotal + valor_frete - desconto, pedido.pagamento.parcelas)
                if pedido.pagamento.metodo == "credito" else Decimal("0")
            )

            # Pagamento simulado: cartão e PIX aprovam na hora; boleto fica pendente
            aprovado = pedido.pagamento.metodo != "boleto"
            cur.execute(
                """UPDATE pedidos
                   SET desconto = %s, valor_frete = %s, juros = %s,
                       status = %s, pago_em = CASE WHEN %s THEN now() END
                   WHERE id = %s
                   RETURNING status, total""",
                (desconto, valor_frete, juros,
                 "pago" if aprovado else "aguardando_pagamento", aprovado, pedido_id),
            )
            status, total = cur.fetchone()

            cur.execute(
                """INSERT INTO pagamentos
                       (pedido_id, metodo, status, valor, parcelas, taxa_juros_mensal, confirmado_em)
                   VALUES (%s, %s, %s, %s, %s, %s, CASE WHEN %s THEN now() END)""",
                (pedido_id, pedido.pagamento.metodo, "aprovado" if aprovado else "pendente",
                 total, pedido.pagamento.parcelas,
                 TAXA_JUROS_MENSAL if juros > 0 else 0, aprovado),
            )
            cur.execute(
                """INSERT INTO entregas
                       (pedido_id, destinatario, logradouro, numero, bairro, cidade,
                        estado, cep, tipo, valor_frete)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (pedido_id, entrega.destinatario, entrega.logradouro or "Não informado",
                 entrega.numero, entrega.bairro or "Não informado", entrega.cidade,
                 entrega.estado.upper(), cep, entrega.tipo, valor_frete),
            )
    except HTTPException:
        raise
    except psycopg.errors.RaiseException as e:
        # Mensagens das procedures (ex.: "Produto indisponivel ou sem estoque")
        raise HTTPException(status_code=409, detail=e.diag.message_primary or "Pedido recusado.")
    except (psycopg.errors.IntegrityError, psycopg.errors.DataError) as e:
        logger.warning("Pedido rejeitado pelo banco: %s", e)
        raise HTTPException(status_code=422, detail="Dados do pedido inválidos.")
    except psycopg.OperationalError as e:
        logger.error("Banco indisponível: %s", e)
        raise HTTPException(status_code=503, detail="Banco de dados indisponível.")

    logger.info("Pedido %s gravado (%s, total %s)", pedido_id, status, total)
    return PedidoOut(pedido_id=pedido_id, status=status, subtotal=subtotal, desconto=desconto,
                     valor_frete=valor_frete, juros=juros, total=total)
