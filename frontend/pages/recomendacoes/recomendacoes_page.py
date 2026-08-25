"""Layout da página Motor de Recomendação (Cross-sell)."""
from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from frontend.components.ui_components import app_shell_with_workflow, button

from frontend.pages.recomendacoes.recomendacoes_components import build_chart_top_produtos, build_filtros, build_grid, build_kpis
from frontend.pages.recomendacoes.recomendacoes_queries import calcular_kpis, carregar_recomendacoes, dados_grafico_top_produtos

def layout(**kwargs) -> html.Div:
    """Monta o layout inicial do Motor de Recomendação (dados atualizados via callback)."""
    df = carregar_recomendacoes()
    kpis = calcular_kpis(df)
    labels, values = dados_grafico_top_produtos(df)

    content = [
        build_filtros(),
        html.Div(id="recomendacoes-kpis-row", children=build_kpis(kpis)),
        html.Div(id="recomendacoes-chart-col", children=build_chart_top_produtos(labels, values)),
        html.Div(id="recomendacoes-grid-col", children=build_grid(df)),
        dcc.Download(id="recomendacoes-download-excel"),
        dbc.Toast(
            id="recomendacoes-toast",
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
            "Exportar Excel", primary=False, icon_key="download", id="recomendacoes-btn-exportar"
        ),
        button(
            "Adicionar ao Pedido",
            primary=True,
            icon_key="cart-plus",
            id="recomendacoes-btn-adicionar-pedido",
            href="/captacao-pedido",
        ),
    ]

    workflow_context = {
        "workflow_id": "recomendacao_para_pedido_flow",
        "step_id": "revisar_recomendacoes",
        "context_data": {},
        "user_role": None,
    }

    return app_shell_with_workflow(
        active_key="recomendacoes",
        icon_key="stars",
        title="Motor de Recomendação (Cross-sell)",
        subtitle="Sugestões de produto por histórico e sazonalidade — nunca criam pedido automaticamente (RN-012)",
        content=content,
        actions=actions,
        workflow_context=workflow_context,
    )


dash.register_page(
    __name__,
    path="/recomendacoes",
    title="Motor de Recomendação (Cross-sell)",
    name="Motor de Recomendação (Cross-sell)",
    layout=layout,
)
