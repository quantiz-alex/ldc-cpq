"""Layout da página Administração (usuários e catálogo) — acesso restrito a admin."""
from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from frontend.components.ui_components import app_shell_with_workflow, button

from frontend.pages.administracao.administracao_components import build_filtros_usuarios, build_grid_catalogo, build_grid_usuarios, build_tabs
from frontend.pages.administracao.administracao_queries import carregar_catalogo, carregar_usuarios


def layout(**kwargs) -> html.Div:
    """Monta o layout inicial da Administração (dados atualizados via callbacks)."""
    df_usuarios = carregar_usuarios()
    df_catalogo = carregar_catalogo()

    usuarios_content = html.Div(
        [
            build_filtros_usuarios(),
            html.Div(id="administracao-grid-usuarios-col", children=build_grid_usuarios(df_usuarios)),
        ],
        className="pt-3",
    )
    catalogo_content = html.Div(
        [html.Div(id="administracao-grid-catalogo-col", children=build_grid_catalogo(df_catalogo))],
        className="pt-3",
    )

    content = [
        build_tabs(usuarios_content, catalogo_content),
        dcc.Store(id="administracao-store-usuario-selecionado", data=None),
        dbc.Toast(
            id="administracao-toast",
            header="Notificação",
            is_open=False,
            dismissable=True,
            duration=4000,
            style={
                "position": "fixed",
                "top": "1rem",
                "right": "1rem",
                "zIndex": 9999,
                "minWidth": "300px",
            },
            color="success",
        ),
    ]

    actions = [
        button(
            "Desativar Usuário Selecionado",
            primary=False,
            icon_key="person-dash",
            id="administracao-btn-desativar-usuario",
        ),
        button("Novo Usuário", primary=True, icon_key="person-plus", id="administracao-btn-novo-usuario"),
        button(
            "Importar CSV (Catálogo)",
            primary=False,
            icon_key="upload",
            id="administracao-btn-importar-csv",
        ),
    ]

    return app_shell_with_workflow(
        active_key="administracao",
        icon_key="people",
        title="Administração",
        subtitle="Controle de usuários do sistema e do catálogo de produtos/preços — restrito a admin",
        content=content,
        actions=actions,
        workflow_context=None,
    )


dash.register_page(
    __name__,
    path="/administracao",
    title="Administração",
    name="Administração",
    layout=layout,
)
