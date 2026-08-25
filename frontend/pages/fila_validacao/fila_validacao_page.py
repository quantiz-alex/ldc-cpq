"""Layout da página Fila de Validação do Trader (screen_type: approval_queue)."""
from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from frontend.components.ui_components import app_shell_with_workflow, button

from frontend.pages.fila_validacao.fila_validacao_components import (
    build_barra_aprovacao,
    build_filtros,
    build_grid,
    build_kpis,
    build_modal_aprovacao,
)
from frontend.pages.fila_validacao.fila_validacao_queries import calcular_kpis_fila, carregar_fila

def layout(**kwargs) -> html.Div:
    """Monta o layout inicial da Fila de Validação (dados atualizados via callbacks)."""
    df = carregar_fila(apenas_pendentes=True)
    kpis = calcular_kpis_fila()

    content = [
        html.Div(id="fila-validacao-kpis-row", children=build_kpis(kpis)),
        build_filtros(),
        build_barra_aprovacao(),
        html.Div(id="fila-validacao-grid-col", children=build_grid(df)),
        build_modal_aprovacao(),
        dcc.Download(id="fila-validacao-download-excel"),
        dbc.Toast(
            id="fila-validacao-toast",
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
            "Exportar Excel", primary=False, icon_key="download", id="fila-validacao-btn-exportar"
        ),
    ]

    workflow_context = {
        "workflow_id": "captacao_aprovacao_flow",
        "step_id": "validar_pedido",
        "context_data": {},
        "user_role": None,
    }

    return app_shell_with_workflow(
        active_key="fila-validacao",
        icon_key="check2-circle",
        title="Fila de Validação do Trader",
        subtitle="Aprove, rejeite ou devolva pedidos enviados pelos RTVs — alertas de consistência já sinalizados (RN-011)",
        content=content,
        actions=actions,
        workflow_context=workflow_context,
    )


dash.register_page(
    __name__,
    path="/fila-validacao",
    title="Fila de Validação do Trader",
    name="Fila de Validação do Trader",
    layout=layout,
)
