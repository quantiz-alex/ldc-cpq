"""Componentes visuais do Dashboard Comercial."""
from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from frontend.components.charts import bar_ranking, multi_line_chart
from frontend.components.ui_components import (
    card,
    filter_card,
    format_currency,
    format_number,
    format_percent,
    kpi_card,
    kpi_row,
)

from frontend.pages.dashboard.dashboard_queries import opcoes_regiao, opcoes_rtv

STATUS_OPTIONS = [
    {"label": s, "value": s}
    for s in ["Rascunho", "Pendente Aprovação", "Aprovado", "Rejeitado", "Devolvido"]
]
LINHA_PRODUTO_OPTIONS = [
    {"label": "Defensivos", "value": "Defensivo"},
    {"label": "Fertilizantes", "value": "Fertilizante"},
]


def build_filtros() -> dbc.Card:
    """Card de filtros do dashboard (período, RTV, região, linha, status)."""
    filtros = [
        dbc.Col(
            [
                dbc.Label("Período", className="small fw-semibold"),
                dcc.DatePickerRange(
                    id="dashboard-filtro-periodo",
                    display_format="DD/MM/YYYY",
                    className="d-block",
                ),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("RTV", className="small fw-semibold"),
                dbc.Select(id="dashboard-filtro-rtv", options=opcoes_rtv(), placeholder="Todos"),
            ],
            md=2,
        ),
        dbc.Col(
            [
                dbc.Label("Região", className="small fw-semibold"),
                dbc.Select(
                    id="dashboard-filtro-regiao", options=opcoes_regiao(), placeholder="Todas"
                ),
            ],
            md=2,
        ),
        dbc.Col(
            [
                dbc.Label("Linha de Produto", className="small fw-semibold"),
                dbc.Select(
                    id="dashboard-filtro-linha-produto",
                    options=LINHA_PRODUTO_OPTIONS,
                    placeholder="Todas",
                ),
            ],
            md=2,
        ),
        dbc.Col(
            [
                dbc.Label("Status", className="small fw-semibold"),
                dbc.Select(
                    id="dashboard-filtro-status", options=STATUS_OPTIONS, placeholder="Todos"
                ),
            ],
            md=2,
        ),
    ]
    return filter_card(filtros, button_id="dashboard-btn-filtrar")


def build_kpis(kpis: dict) -> dbc.Row:
    """Monta a fileira de KPI cards do dashboard."""
    cards = [
        kpi_card(
            "Pedidos Captados",
            format_number(kpis["pedidos_captados"]),
            format_number(kpis["pedidos_captados"]),
            0.0,
            "neutral",
        ),
        kpi_card(
            "Receita Acumulada",
            format_currency(kpis["receita_acumulada"]),
            format_currency(kpis["receita_acumulada"]),
            0.0,
            "neutral",
        ),
        kpi_card(
            "Ticket Médio",
            format_currency(kpis["ticket_medio"]),
            format_currency(kpis["ticket_medio"]),
            0.0,
            "neutral",
        ),
        kpi_card(
            "Pendentes de Validação",
            format_number(kpis["pendentes_validacao"]),
            format_number(kpis["pendentes_validacao"]),
            0.0,
            "neutral",
        ),
        kpi_card(
            "Tempo Médio de Triagem",
            f"{kpis['tempo_medio_triagem']:.1f} dias",
            f"{kpis['tempo_medio_triagem']:.1f} dias",
            0.0,
            "neutral",
        ),
        kpi_card(
            "% Com Alerta",
            format_percent(kpis["pct_com_alerta"], with_sign=False),
            format_percent(kpis["pct_com_alerta"], with_sign=False),
            0.0,
            "neutral",
        ),
    ]
    return kpi_row(cards)


def build_chart_receita(x: list, series: dict) -> dbc.Card:
    """Card com gráfico de linha de receita semanal por linha de produto."""
    fig = multi_line_chart(
        x, series, title="", x_label="Semana", y_label="Receita (R$)", height=300
    )
    return card(
        "Evolução de Receita — Defensivos x Fertilizantes",
        dcc.Graph(id="dashboard-chart-receita", figure=fig, config={"displayModeBar": False}),
    )


def build_chart_top_rtv(labels: list, values: list) -> dbc.Card:
    """Card com ranking de Top RTVs por receita captada."""
    fig = bar_ranking(labels, values, value_fmt=lambda v: format_currency(v), height=300)
    return card(
        "Top RTVs por Receita Captada",
        dcc.Graph(id="dashboard-chart-top-rtv", figure=fig, config={"displayModeBar": False}),
    )
