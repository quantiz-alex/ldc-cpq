"""Sidebar fixa da aplicação — navegação entre as telas do LDC Insumos CPQ."""
from __future__ import annotations

import dash_bootstrap_components as dbc
import json
import os
from pathlib import Path
from dash import Input, Output, callback, html

# ============================================================================
# BRANDING — lido de .build/project.json e docs/design-system.yaml
# ============================================================================

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_PROJECT_JSON = _PROJECT_ROOT / ".build" / "project.json"

try:
    _project_data = json.loads(_PROJECT_JSON.read_text(encoding="utf-8"))
    _branding = _project_data.get("branding", {})
except (FileNotFoundError, json.JSONDecodeError):
    _branding = {}

PRIMARY_COLOR: str = _branding.get("primary", "#1045C8")
DISPLAY_NAME: str = _branding.get("display_name", "LDC Insumos")
_LOGO_RAW: str | None = _branding.get("logo")
_LOGO_FILENAME: str | None = (
    _LOGO_RAW[len("assets/"):] if _LOGO_RAW and _LOGO_RAW.startswith("assets/") else _LOGO_RAW
)

_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
_LOGO_EXISTS = (
    os.path.isfile(os.path.join(_ASSETS_DIR, _LOGO_FILENAME)) if _LOGO_FILENAME else False
)

# ============================================================================
# NAVEGAÇÃO — uma entrada por página
# ============================================================================

NAV_ITEMS: list[dict] = [
    {"key": "dashboard", "label": "Dashboard Comercial", "icon": "speedometer2", "href": "/dashboard"},
    {"key": "captacao-pedido", "label": "Captação de Pedido", "icon": "cart-plus", "href": "/captacao-pedido"},
    {"key": "recomendacoes", "label": "Recomendações", "icon": "stars", "href": "/recomendacoes"},
    {"key": "relatorios", "label": "Relatórios", "icon": "file-earmark-bar-graph", "href": "/relatorios"},
    {"key": "fila-validacao", "label": "Fila de Validação", "icon": "check2-circle", "href": "/fila-validacao"},
    {"key": "administracao", "label": "Administração", "icon": "people", "href": "/administracao"},
]

CONTENT_STYLE: dict = {"marginLeft": "240px"}
CONTENT_FULL_STYLE: dict = {"marginLeft": "0"}


def _build_topo() -> html.Div:
    """Logo mark (imagem ou badge com iniciais) + nome do projeto."""
    if _LOGO_EXISTS:
        marca: html.Img | html.Div = html.Img(
            src=f"/assets/{_LOGO_FILENAME}",
            height=64,
            style={"objectFit": "contain", "maxWidth": "180px"},
        )
    else:
        marca = html.Div(
            DISPLAY_NAME[:2].upper(),
            style={
                "width": "48px",
                "height": "48px",
                "borderRadius": "8px",
                "background": PRIMARY_COLOR,
                "color": "#ffffff",
                "fontSize": "1rem",
                "fontWeight": "800",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "flexShrink": "0",
            },
        )

    return html.Div(
        [marca],
        style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "padding": "1.5rem 1.25rem 1.25rem",
        },
    )


def _build_rodape() -> html.Div:
    """Rodapé com atribuição da Quantiz Pricing Solution."""
    return html.Div(
        [
            html.Div("Desenvolvido por", style={"fontWeight": 500}),
            html.Div("Quantiz Pricing Solution", style={"fontWeight": 500}),
        ],
        style={
            "color": "#94a3b8",
            "fontSize": "0.72rem",
            "padding": "0.875rem 1.25rem",
            "borderTop": "1px solid #e2e8f0",
            "lineHeight": "1.6",
        },
    )


def build_sidebar(pathname: str = "/") -> html.Div:
    """Monta a sidebar fixa (240px) com navegação e rodapé."""
    nav_links = [
        dbc.NavLink(
            [html.I(className=f"bi bi-{item['icon']}"), item["label"]],
            href=item["href"],
            active="exact",
            className="nav-link",
        )
        for item in NAV_ITEMS
    ]

    return html.Div(
        [
            _build_topo(),
            html.Hr(style={"margin": "0 0.75rem 0.5rem", "borderColor": "#e2e8f0", "opacity": "1"}),
            html.Nav(dbc.Nav(nav_links, vertical=True), className="sidebar-nav flex-grow-1 py-2"),
            _build_rodape(),
        ],
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "240px",
            "background": "#ffffff",
            "borderRight": "1px solid #e2e8f0",
            "boxShadow": "2px 0 8px rgba(0,0,0,0.04)",
            "display": "flex",
            "flexDirection": "column",
            "zIndex": 1000,
            "overflowY": "auto",
        },
    )


def register_sidebar_callbacks() -> None:
    """Nenhum callback dedicado — build_sidebar é chamada por toggle_sidebar em app.py."""
    return None
