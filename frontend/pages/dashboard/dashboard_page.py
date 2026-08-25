"""Layout da página Dashboard Comercial."""
from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from frontend.components.ui_components import app_shell_with_workflow, button

from frontend.pages.dashboard.dashboard_components import build_chart_receita, build_chart_top_rtv, build_filtros, build_kpis
from frontend.pages.dashboard.dashboard_queries import calcular_kpis, carregar_pedidos, dados_grafico_receita_semana, dados_grafico_top_rtv

def layout(**kwargs) -> html.Div:
    """Monta o layout inicial do Dashboard Comercial (dados atualizados via callback de filtro)."""
    df = carregar_pedidos()
    kpis = calcular_kpis(df)
    x, series = dados_grafico_receita_semana(df)
    labels, values = dados_grafico_top_rtv(df)

    content = [
        build_filtros(),
        html.Div(id="dashboard-kpis-row", children=build_kpis(kpis)),
        dbc.Row(
            [
                dbc.Col(build_chart_receita(x, series), md=7, id="dashboard-chart-receita-col"),
                dbc.Col(build_chart_top_rtv(labels, values), md=5, id="dashboard-chart-top-rtv-col"),
            ]
        ),
        dcc.Download(id="dashboard-download-excel"),
        dbc.Toast(
            id="dashboard-toast",
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
            "Exportar Excel", primary=False, icon_key="download", id="dashboard-btn-exportar"
        ),
        button(
            "Ver Pedidos",
            primary=True,
            icon_key="arrow-right-circle",
            id="dashboard-btn-drilldown",
            href="/fila-validacao",
        ),
    ]

    workflow_context = {
        "workflow_id": "captacao_aprovacao_flow",
        "step_id": "monitorar_dashboard",
        "context_data": {},
        "user_role": None,
    }

    return app_shell_with_workflow(
        active_key="dashboard",
        icon_key="speedometer2",
        title="Dashboard Comercial",
        subtitle="Volume de pedidos, receita, mix defensivos x fertilizantes e desempenho por RTV/região",
        content=content,
        actions=actions,
        workflow_context=workflow_context,
    )


dash.register_page(
    __name__,
    path="/dashboard",
    title="Dashboard Comercial",
    name="Dashboard Comercial",
    layout=layout,
)
