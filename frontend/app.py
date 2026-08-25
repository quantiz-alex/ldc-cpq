"""Aplicação Dash — LDC Insumos, Plataforma Comercial (CPQ Inteligente)."""
from __future__ import annotations

import os
from urllib.parse import parse_qs

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html, no_update

from frontend.components.sidebar import (
    CONTENT_FULL_STYLE,
    CONTENT_STYLE,
    build_sidebar,
    register_sidebar_callbacks,
)

# 1. Instanciar app PRIMEIRO
_ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

app = dash.Dash(
    __name__,
    use_pages=True,
    # pages_folder="" desativa o auto-scan de diretório do Dash (que duplicaria o
    # registro de cada página sob o módulo sintético "pages.*"); dash.register_page()
    # continua funcionando pois cada <pagina>_page.py é importado manualmente abaixo
    # sob o namespace real "frontend.pages.*".
    pages_folder="",
    assets_folder=_ASSETS,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
    ],
    suppress_callback_exceptions=True,
    title="LDC Insumos — Plataforma Comercial (CPQ Inteligente)",
)
server = app.server

# 2. Importar layouts APÓS app (aciona dash.register_page() em cada módulo)
from frontend.pages.login.login_page import layout as login_layout  # noqa: E402
from frontend.pages.dashboard.dashboard_page import layout as dashboard_layout  # noqa: E402
from frontend.pages.captacao_pedido.captacao_pedido_page import layout as captacao_pedido_layout  # noqa: E402
from frontend.pages.captacao_pedido.captacao_pedido_form_page import (  # noqa: E402
    layout as captacao_pedido_form_layout,
)
from frontend.pages.fila_validacao.fila_validacao_page import layout as fila_validacao_layout  # noqa: E402
from frontend.pages.recomendacoes.recomendacoes_page import layout as recomendacoes_layout  # noqa: E402
from frontend.pages.relatorios.relatorios_page import layout as relatorios_layout  # noqa: E402
from frontend.pages.administracao.administracao_page import layout as administracao_layout  # noqa: E402

_PAGE_LAYOUTS: dict = {
    "/": login_layout,
    "/login": login_layout,
    "/dashboard": dashboard_layout,
    "/captacao-pedido": captacao_pedido_layout,
    "/captacao-pedido/novo-pedido": captacao_pedido_form_layout,
    "/fila-validacao": fila_validacao_layout,
    "/recomendacoes": recomendacoes_layout,
    "/relatorios": relatorios_layout,
    "/administracao": administracao_layout,
}

_PROTEGIDAS = [
    "/dashboard",
    "/captacao-pedido",
    "/captacao-pedido/novo-pedido",
    "/fila-validacao",
    "/recomendacoes",
    "/relatorios",
    "/administracao",
]

# 3. Imports de callbacks
from frontend.pages.login.login_callbacks import register_callbacks as login_register  # noqa: E402
from frontend.pages.dashboard.dashboard_callbacks import register_callbacks as dashboard_register  # noqa: E402
from frontend.pages.captacao_pedido.captacao_pedido_callbacks import (  # noqa: E402
    register_callbacks as captacao_pedido_register,
)
from frontend.pages.captacao_pedido.captacao_pedido_form_callbacks import (  # noqa: E402
    register_callbacks as captacao_pedido_form_register,
)
from frontend.pages.fila_validacao.fila_validacao_callbacks import (  # noqa: E402
    register_callbacks as fila_validacao_register,
)
from frontend.pages.recomendacoes.recomendacoes_callbacks import (  # noqa: E402
    register_callbacks as recomendacoes_register,
)
from frontend.pages.relatorios.relatorios_callbacks import register_callbacks as relatorios_register  # noqa: E402
from frontend.pages.administracao.administracao_callbacks import (  # noqa: E402
    register_callbacks as administracao_register,
)

# 4. Layout — SEM dash.page_container
app.layout = html.Div(
    [
        dcc.Store(id="current-user", storage_type="session"),
        dcc.Location(id="url", refresh=False),
        html.Div(id="sidebar-wrapper"),
        html.Div(html.Div(id="page-content"), id="main-content"),
    ]
)

# 5. Registrar callbacks
login_register()
dashboard_register()
captacao_pedido_register()
captacao_pedido_form_register()
fila_validacao_register()
recomendacoes_register()
relatorios_register()
administracao_register()
register_sidebar_callbacks()


# 6. Render de página
_ROTAS_SOMENTE_ADMIN = ["/administracao"]  # RN-016 — somente admin acessa Administração


@callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("url", "search"),
    Input("current-user", "data"),
    prevent_initial_call=False,
)
def render_page_content(pathname: str, search: str, user_data):
    if pathname in _ROTAS_SOMENTE_ADMIN and (not user_data or user_data.get("role") != "admin"):
        return dbc.Alert(
            "Acesso restrito a administradores (RN-016).", color="danger", className="m-4"
        )

    layout_fn = _PAGE_LAYOUTS.get(pathname)
    if layout_fn is None:
        return dbc.Alert(f"Página não encontrada: {pathname}", color="warning", className="m-4")
    if not callable(layout_fn):
        return layout_fn

    # Query string (?pedido_id=N etc.) repassada como kwargs para a página já
    # nascer populada — evita callback de "população" correndo contra a troca de rota.
    query_params = {k: v[0] for k, v in parse_qs((search or "").lstrip("?")).items()}
    return layout_fn(**query_params)


# 7. Guard routes — callback "base" de url.pathname; navegação disparada por ações
# do usuário (ex.: captacao_pedido_callbacks.py) usa Output(..., allow_duplicate=True)
@callback(
    Output("url", "pathname"),
    Input("url", "pathname"),
    Input("current-user", "data"),
    prevent_initial_call=False,
)
def guard_routes(pathname: str, user_data):
    if pathname in ("/", None):
        return "/dashboard" if user_data else "/login"
    if pathname == "/login":
        return "/dashboard" if user_data else no_update
    if pathname in _PROTEGIDAS:
        return no_update if user_data else "/login"
    return no_update


# 8. Toggle sidebar
@callback(
    Output("sidebar-wrapper", "children"),
    Output("main-content", "style"),
    Input("url", "pathname"),
    Input("current-user", "data"),
    prevent_initial_call=False,
)
def toggle_sidebar(pathname: str, user_data):
    if pathname in ("/login", "/") or not user_data:
        return [], CONTENT_FULL_STYLE
    return build_sidebar(pathname), CONTENT_STYLE


if __name__ == "__main__":
    app.run(debug=True, port=1050)
