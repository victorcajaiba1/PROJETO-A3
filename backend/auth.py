"""Autenticação mínima do administrador para as rotas que alteram o catálogo.

O login de clientes ainda acontece no navegador. Para escrever no banco, o
admin informa a senha definida na variável ADMIN_PASSWORD e recebe um token
assinado (HMAC) válido por algumas horas.
"""

import base64
import hashlib
import hmac
import os
import time

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
_CHAVE = hashlib.sha256(
    (os.getenv("SECRET_KEY") or "techwear:" + ADMIN_PASSWORD).encode()
).digest()
VALIDADE_SEGUNDOS = 12 * 60 * 60

router = APIRouter()


class LoginIn(BaseModel):
    senha: str


def _assinar(conteudo: str) -> str:
    return hmac.new(_CHAVE, conteudo.encode(), hashlib.sha256).hexdigest()


def gerar_token() -> str:
    expira = str(int(time.time()) + VALIDADE_SEGUNDOS)
    corpo = base64.urlsafe_b64encode(f"admin|{expira}".encode()).decode()
    return f"{corpo}.{_assinar(corpo)}"


def token_valido(token: str) -> bool:
    try:
        corpo, assinatura = token.split(".", 1)
        if not hmac.compare_digest(assinatura, _assinar(corpo)):
            return False
        papel, expira = base64.urlsafe_b64decode(corpo).decode().split("|")
        return papel == "admin" and int(expira) > time.time()
    except (ValueError, UnicodeDecodeError):
        return False


def exigir_admin(authorization: str = Header(default="")) -> None:
    """Dependência das rotas de escrita: exige 'Authorization: Bearer <token>'."""
    if not ADMIN_PASSWORD:
        raise HTTPException(status_code=503, detail="ADMIN_PASSWORD não configurada no servidor.")
    token = authorization.removeprefix("Bearer ").strip()
    if not token or not token_valido(token):
        raise HTTPException(status_code=401, detail="Login de administrador necessário.")


@router.post("/admin/login")
def login_admin(dados: LoginIn):
    if not ADMIN_PASSWORD:
        raise HTTPException(status_code=503, detail="ADMIN_PASSWORD não configurada no servidor.")
    if not hmac.compare_digest(dados.senha.encode(), ADMIN_PASSWORD.encode()):
        time.sleep(1)  # atrasa tentativas de força bruta
        raise HTTPException(status_code=401, detail="Senha de administrador incorreta.")
    return {"token": gerar_token(), "expira_em": VALIDADE_SEGUNDOS}
