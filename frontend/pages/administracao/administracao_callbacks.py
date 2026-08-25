"""Callbacks da página Administração — RN-016 (gate admin) e RN-017 (email único)."""
from __future__ import annotations

from dash import Input, Output, State, callback, no_update

from frontend.pages.administracao.administracao_components import build_grid_usuarios
from frontend.pages.administracao.administracao_queries import carregar_usuarios, desativar_usuario


def register_callbacks() -> None:
    """Registra todos os callbacks da página Administração."""

    # [Padrão 1] Filtrar grid de usuários
    @callback(
        Output("administracao-grid-usuarios-col", "children"),
        Input("administracao-btn-filtrar", "n_clicks"),
        State("administracao-filtro-role", "value"),
        State("administracao-filtro-ativo", "value"),
        prevent_initial_call=False,
    )
    def atualizar_grid_usuarios(n_clicks: int, role: str | None, ativo: str | None):
        df = carregar_usuarios(role=role, ativo=ativo)
        return build_grid_usuarios(df)

    # ── Selecionar usuário na grid (para desativação) ─────────────────────
    @callback(
        Output("administracao-store-usuario-selecionado", "data"),
        Input("administracao-grid-usuarios", "cellClicked"),
        prevent_initial_call=True,
    )
    def selecionar_usuario(cell_clicked: dict):
        if not cell_clicked:
            return no_update
        return cell_clicked.get("rowData", {}).get("id")

    # ── Desativar usuário (RN-016 — somente admin) ─────────────────────────
    @callback(
        Output("administracao-grid-usuarios-col", "children", allow_duplicate=True),
        Output("administracao-toast", "is_open"),
        Output("administracao-toast", "children"),
        Output("administracao-toast", "color"),
        Input("administracao-btn-desativar-usuario", "n_clicks"),
        State("administracao-store-usuario-selecionado", "data"),
        State("current-user", "data"),
        State("administracao-filtro-role", "value"),
        State("administracao-filtro-ativo", "value"),
        prevent_initial_call=True,
    )
    def desativar_usuario_selecionado(
        n_clicks: int,
        usuario_id: int | None,
        user_data: dict | None,
        role_filtro: str | None,
        ativo_filtro: str | None,
    ):
        if not n_clicks:
            return no_update, False, "", "success"

        if not user_data or user_data.get("role") != "admin":
            return no_update, True, "Somente admin pode desativar usuários (RN-016).", "danger"

        if usuario_id is None:
            return no_update, True, "Selecione um usuário na grid antes de desativar.", "warning"

        desativar_usuario(int(usuario_id))
        df = carregar_usuarios(role=role_filtro, ativo=ativo_filtro)
        return build_grid_usuarios(df), True, f"Usuário #{usuario_id} desativado.", "success"
