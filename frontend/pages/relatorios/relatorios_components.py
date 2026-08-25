"""Componentes visuais de Relatórios Comerciais."""
from __future__ import annotations

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc

from frontend.components.charts import bar_ranking, multi_line_chart
from frontend.components.ui_components import card, data_table, filter_card

from frontend.pages.relatorios.relatorios_queries import opcoes_cliente, opcoes_linha_produto, opcoes_regiao, opcoes_rtv


def build_filtros() -> dbc.Card:
    """Card de filtros do relatório (período, RTV, região, cliente, linha)."""
    filtros = [
        dbc.Col(
            [
                dbc.Label("Período", className="small fw-semibold"),
                dcc.DatePickerRange(id="relatorios-filtro-periodo", display_format="DD/MM/YYYY", className="d-block"),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("RTV", className="small fw-semibold"),
                dbc.Select(id="relatorios-filtro-rtv", options=opcoes_rtv(), placeholder="Todos"),
            ],
            md=2,
        ),
        dbc.Col(
            [
                dbc.Label("Região", className="small fw-semibold"),
                dbc.Select(id="relatorios-filtro-regiao", options=opcoes_regiao(), placeholder="Todas"),
            ],
            md=2,
        ),
        dbc.Col(
            [
                dbc.Label("Cliente", className="small fw-semibold"),
                dbc.Select(id="relatorios-filtro-cliente", options=opcoes_cliente(), placeholder="Todos"),
            ],
            md=2,
        ),
        dbc.Col(
            [
                dbc.Label("Linha de Produto", className="small fw-semibold"),
                dbc.Select(
                    id="relatorios-filtro-linha-produto", options=opcoes_linha_produto(), placeholder="Todas"
                ),
            ],
            md=2,
        ),
    ]
    return filter_card(filtros, button_id="relatorios-btn-filtrar")


def build_chart_receita(x: list, series: dict) -> dbc.Card:
    """Card com gráfico de linha de receita por período, quebrado por RTV (top 5)."""
    fig = multi_line_chart(x, series, x_label="Mês", y_label="Receita (R$)", height=300)
    return card("Receita por Período e RTV", dcc.Graph(id="relatorios-chart-receita", figure=fig, config={"displayModeBar": False}))


def build_chart_eficiencia(labels: list, values: list) -> dbc.Card:
    """Card com gráfico de barras de eficiência de triagem (contagem por status)."""
    fig = bar_ranking(labels, values, value_fmt=lambda v: f"{int(v)}", height=300)
    return card(
        "Eficiência de Triagem (contagem por status)",
        dcc.Graph(id="relatorios-chart-eficiencia", figure=fig, config={"displayModeBar": False}),
    )


def build_grid(df: pd.DataFrame) -> dbc.Card:
    """Grid detalhada de pedidos e receita do período filtrado."""
    grid = data_table(df, id="relatorios-grid", numeric_cols=["valor_total"], status_col="status")
    return card("Pedidos e Receita", grid)
