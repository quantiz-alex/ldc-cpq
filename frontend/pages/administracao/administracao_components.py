"""Componentes visuais da Administração (usuários e catálogo)."""
from __future__ import annotations

import dash_bootstrap_components as dbc
import pandas as pd

from frontend.components.ui_components import card, data_table, filter_card

from frontend.pages.administracao.administracao_queries import opcoes_role

ATIVO_OPTIONS = [{"label": "Sim", "value": "Sim"}, {"label": "Não", "value": "Não"}]


def build_filtros_usuarios() -> dbc.Card:
    """Card de filtros da aba Usuários (perfil, ativo)."""
    filtros = [
        dbc.Col(
            [
                dbc.Label("Perfil", className="small fw-semibold"),
                dbc.Select(id="administracao-filtro-role", options=opcoes_role(), placeholder="Todos"),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("Ativo", className="small fw-semibold"),
                dbc.Select(id="administracao-filtro-ativo", options=ATIVO_OPTIONS, placeholder="Todos"),
            ],
            md=3,
        ),
    ]
    return filter_card(filtros, button_id="administracao-btn-filtrar")


def build_grid_usuarios(df: pd.DataFrame) -> dbc.Card:
    """Grid de usuários — RN-016/RN-017."""
    grid = data_table(df, id="administracao-grid-usuarios", numeric_cols=[], status_col="ativo")
    return card("Usuários", grid)


def build_grid_catalogo(df: pd.DataFrame) -> dbc.Card:
    """Grid de catálogo de produtos."""
    grid = data_table(
        df, id="administracao-grid-catalogo", numeric_cols=["custo"], status_col="ativo"
    )
    return card("Catálogo de Produtos", grid)


def build_tabs(usuarios_content, catalogo_content) -> dbc.Tabs:
    """Abas Usuários / Catálogo."""
    return dbc.Tabs(
        [
            dbc.Tab(usuarios_content, label="Usuários", tab_id="administracao-tab-usuarios"),
            dbc.Tab(catalogo_content, label="Catálogo", tab_id="administracao-tab-catalogo"),
        ],
        id="administracao-tabs",
        active_tab="administracao-tab-usuarios",
        className="mb-3",
    )
