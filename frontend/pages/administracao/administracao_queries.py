"""Consultas e regras de dados da Administração (usuários e catálogo).

RN-016: somente admin pode criar/editar/desativar usuários e editar o catálogo.
RN-017: email deve ser único no sistema.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent.parent / "mock_data"

_USUARIOS_CSV = DATA_DIR / "usuarios.csv"
_PRODUTOS_CSV = DATA_DIR / "produtos.csv"


def carregar_usuarios(role: str | None = None, ativo: str | None = None) -> pd.DataFrame:
    """Retorna usuários filtrados por perfil e status ativo."""
    df = pd.read_csv(_USUARIOS_CSV)
    if role:
        df = df[df["role"] == role]
    if ativo is not None and ativo != "":
        valor = 1 if ativo == "Sim" else 0
        df = df[df["ativo"] == valor]

    df = df.copy()
    df["ativo"] = df["ativo"].map({1: "Sim", 0: "Não", True: "Sim", False: "Não"})
    colunas = ["id", "nome", "email", "role", "rtv_territorio", "ativo"]
    return df[colunas]


def carregar_catalogo() -> pd.DataFrame:
    """Retorna o catálogo de produtos para a aba Catálogo."""
    df = pd.read_csv(_PRODUTOS_CSV)
    df = df.copy()
    df["ativo"] = df["ativo"].map({1: "Sim", 0: "Não", True: "Sim", False: "Não"})
    colunas = ["id", "nome_comercial", "tipo", "classe", "unidade", "custo", "ativo"]
    return df[colunas]


def email_existe(email: str, ignorar_id: int | None = None) -> bool:
    """RN-017 — verifica unicidade de email antes de criar/editar usuário."""
    df = pd.read_csv(_USUARIOS_CSV)
    if ignorar_id is not None:
        df = df[df["id"] != ignorar_id]
    return bool((df["email"].str.lower() == email.lower()).any())


def desativar_usuario(usuario_id: int) -> None:
    """RN-016 — apenas admin (garantido no callback) pode desativar usuário."""
    df = pd.read_csv(_USUARIOS_CSV)
    mascara = df["id"] == usuario_id
    df.loc[mascara, "ativo"] = 0
    df.loc[mascara, "updated_at"] = datetime.now().isoformat(timespec="seconds")
    df.to_csv(_USUARIOS_CSV, index=False)


def opcoes_role() -> list[dict]:
    """Opções de perfil (role) para o filtro dropdown."""
    return [
        {"label": "Admin", "value": "admin"},
        {"label": "Trader", "value": "trader"},
        {"label": "RTV", "value": "rtv"},
    ]
