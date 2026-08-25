"""Layout da página Captação de Pedido (CPQ).

NÃO é uma tela de simulação: nenhuma regra logic_type: interactive_formula está
vinculada ao módulo "Captação de Pedido (CPQ)" em docs/business_logic.yaml — RN-004
(precificação) é logic_type: derived_field, resolvida por fórmula determinística
(preco_base × % condição × % janela), sem slider/painel de parâmetros interativos.
"""
from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from frontend.components.ui_components import app_shell_with_workflow, button

from frontend.pages.captacao_pedido.captacao_pedido_components import (
    build_grid_rascunhos,
    build_modal_captura_assistida,
)
from frontend.pages.captacao_pedido.captacao_pedido_queries import carregar_pedidos_em_aberto

def layout(**kwargs) -> html.Div:
    """Monta o layout inicial da Captação de Pedido (dados atualizados via callbacks).

    A criação/edição de pedido (Cabeçalho, Adicionar Item, Itens do Pedido) vive em
    rota própria (/captacao-pedido/novo-pedido) — modal era pequeno demais para a
    grid de itens.
    """
    df_rascunhos = carregar_pedidos_em_aberto()

    content = [
        html.Div(id="captacao-pedido-grid-rascunhos-col", children=build_grid_rascunhos(df_rascunhos)),
        build_modal_captura_assistida(),
        dbc.Toast(
            id="captacao-pedido-toast",
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
            "Captura Assistida",
            primary=False,
            icon_key="chat-left-text",
            id="captacao-pedido-btn-importar-mensagem",
        ),
        button(
            "Novo Pedido",
            primary=True,
            icon_key="plus-circle",
            id="captacao-pedido-btn-novo",
        ),
    ]

    workflow_context = {
        "workflow_id": "captacao_aprovacao_flow",
        "step_id": "capturar_pedido",
        "context_data": {},
        "user_role": None,
    }

    return app_shell_with_workflow(
        active_key="captacao-pedido",
        icon_key="cart-plus",
        title="Captação de Pedido (CPQ)",
        subtitle=(
            "Cliente, itens e condições comerciais — o preço unitário é sempre "
            "calculado automaticamente por produto + janela de entrega + condição (RN-004)"
        ),
        content=content,
        actions=actions,
        workflow_context=workflow_context,
    )


dash.register_page(
    __name__,
    path="/captacao-pedido",
    title="Captação de Pedido (CPQ)",
    name="Captação de Pedido (CPQ)",
    layout=layout,
)
