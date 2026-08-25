"""Página de criação/edição de pedido (Captação de Pedido — CPQ).

Rota própria em vez de modal: a grid de Itens do Pedido (RN-004) precisa de mais
espaço do que um modal comporta. O pedido a exibir vem sempre pela query string
(?pedido_id=N) — assim o formulário já nasce populado no primeiro render, sem
depender de um callback de "população" que poderia perder a corrida contra a troca
de rota em um app multi-página.
"""
from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from frontend.components.ui_components import app_shell

from frontend.pages.captacao_pedido.captacao_pedido_components import (
    build_form_cabecalho,
    build_form_item,
    build_grid_itens,
    build_modal_confirmar_saida,
)
from frontend.pages.captacao_pedido.captacao_pedido_queries import (
    carregar_cabecalho_pedido,
    carregar_itens_pedido,
)

STORE_PEDIDO_ID = "captacao-pedido-store-pedido-ativo"


def layout(pedido_id: str | None = None, **kwargs) -> html.Div:
    """Monta o formulário do pedido indicado por ?pedido_id= (já populado)."""
    pedido_id_int = int(pedido_id) if pedido_id else None
    cabecalho = carregar_cabecalho_pedido(pedido_id_int) if pedido_id_int else {}
    df_itens = carregar_itens_pedido(pedido_id_int if pedido_id_int is not None else -1)

    titulo = f"Pedido #{pedido_id_int}" if pedido_id_int else "Novo Pedido"

    content = [
        dcc.Store(id=STORE_PEDIDO_ID, data=pedido_id_int),
        html.Div(
            id="captacao-pedido-form-cabecalho-col",
            children=build_form_cabecalho(cabecalho),
        ),
        html.Div(
            id="captacao-pedido-form-item-col",
            children=build_form_item(),
            className="mt-3",
        ),
        html.Div(
            id="captacao-pedido-grid-itens-col",
            children=build_grid_itens(df_itens),
            className="mt-3",
        ),
        build_modal_confirmar_saida(),
        dbc.Toast(
            id="captacao-pedido-form-toast",
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
        dbc.Button(
            [html.I(className="bi bi-arrow-left me-2"), "Voltar"],
            id="captacao-pedido-form-btn-voltar",
            color="secondary",
            outline=True,
        ),
        dbc.Button(
            [html.I(className="bi bi-send me-2"), "Enviar para Validação"],
            id="captacao-pedido-btn-enviar-aprovacao",
            color="primary",
            className="fw-bold",
        ),
    ]

    return app_shell(
        active_key="captacao-pedido",
        icon_key="cart-plus",
        title=titulo,
        subtitle=(
            "Cliente, itens e condições comerciais — o preço unitário é sempre "
            "calculado automaticamente por produto + janela de entrega + condição (RN-004)"
        ),
        content=content,
        actions=actions,
    )


dash.register_page(
    __name__,
    path="/captacao-pedido/novo-pedido",
    title="Pedido — Captação (CPQ)",
    name="Novo Pedido",
    layout=layout,
)
