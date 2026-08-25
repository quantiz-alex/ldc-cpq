"""Callbacks da página de Login — validação de email em modo mock."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from dash import Input, Output, State, callback, ctx, no_update

DATA_DIR = Path(__file__).parent.parent.parent.parent / "mock_data"
_USUARIOS_CSV = DATA_DIR / "usuarios.csv"


def register_callbacks() -> None:
    """Registra os callbacks da página de login."""

    @callback(
        Output("current-user", "data"),
        Output("login-alert", "children"),
        Output("login-alert", "is_open"),
        Input("login-btn", "n_clicks"),
        Input("login-senha", "n_submit"),
        State("login-email", "value"),
        State("login-senha", "value"),
        prevent_initial_call=True,
    )
    def autenticar(n_clicks: int, n_submit: int, email: str | None, senha: str | None) -> tuple:
        if not ctx.triggered:
            return no_update, no_update, no_update

        if not email:
            return no_update, "Informe o email cadastrado.", True

        usuarios = pd.read_csv(_USUARIOS_CSV)
        mascara = usuarios["email"].str.lower() == email.strip().lower()
        encontrado = usuarios[mascara]

        if encontrado.empty:
            return no_update, "Email não encontrado. Verifique mock_data/usuarios.csv.", True

        usuario = encontrado.iloc[0]
        if usuario["ativo"] not in (1, True):
            return no_update, "Usuário inativo — contate o administrador.", True

        user_data = {
            "id": int(usuario["id"]),
            "nome": usuario["nome"],
            "email": usuario["email"],
            "role": usuario["role"],
            "rtv_territorio": usuario["rtv_territorio"] if pd.notna(usuario["rtv_territorio"]) else None,
        }
        return user_data, "", False
