"""Layout da página Relatórios Comerciais."""
from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from frontend.components.ui_components import app_shell_with_workflow, button

from frontend.pages.relatorios.relatorios_components import build_chart_eficiencia, build_chart_receita, build_filtros, build_grid
from frontend.pages.relatorios.relatorios_queries import carregar_relatorio, dados_grafico_eficiencia, dados_grafico_receita_periodo

def layout(**kwargs) -> html.Div:
    """Monta o layout inicial de Relatórios Comerciais (dados atualizados via callback)."""
    df = carregar_relatorio()
    x, series = dados_grafico_receita_periodo(df)
    labels, values = dados_grafico_eficiencia(df)

    content = [
        build_filtros(),
        dbc.Row(
            [
                dbc.Col(build_chart_receita(x, series), md=7, id="relatorios-chart-receita-col"),
                dbc.Col(build_chart_eficiencia(labels, values), md=5, id="relatorios-chart-eficiencia-col"),
            ]
        ),
        html.Div(id="relatorios-grid-col", children=build_grid(df)),
        dcc.Download(id="relatorios-download-excel"),
        dbc.Toast(
            id="relatorios-toast",
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
            "Exportar Excel", primary=True, icon_key="download", id="relatorios-btn-exportar-excel"
        ),
        button(
            "Exportar PDF", primary=False, icon_key="file-earmark-pdf", id="relatorios-btn-exportar-pdf"
        ),
    ]

    workflow_context = {
        "workflow_id": "reporting_flow",
        "step_id": "relatorio_step",
        "context_data": {},
        "user_role": None,
    }

    return app_shell_with_workflow(
        active_key="relatorios",
        icon_key="file-earmark-bar-graph",
        title="Relatórios Comerciais",
        subtitle="Pedidos, receita, mix de produtos, desempenho de RTVs e taxa de aprovação/rejeição",
        content=content,
        actions=actions,
        workflow_context=workflow_context,
    )


dash.register_page(
    __name__,
    path="/relatorios",
    title="Relatórios Comerciais",
    name="Relatórios Comerciais",
    layout=layout,
)
