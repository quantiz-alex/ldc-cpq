"""Componentes visuais do Motor de Recomendação (Cross-sell)."""
from __future__ import annotations

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc

from frontend.components.charts import bar_ranking
from frontend.components.ui_components import (
    card,
    data_table,
    filter_card,
    format_currency,
    format_percent,
    kpi_card,
    kpi_row,
)

from frontend.pages.recomendacoes.recomendacoes_queries import opcoes_clientes, opcoes_cultura_safra, opcoes_linha_produto, opcoes_regiao


def build_filtros() -> dbc.Card:
    """Card de filtros de recomendações (cliente, cultura/safra, região, linha)."""
    filtros = [
        dbc.Col(
            [
                dbc.Label("Cliente", className="small fw-semibold"),
                dbc.Select(id="recomendacoes-filtro-cliente", options=opcoes_clientes(), placeholder="Todos"),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("Cultura/Safra", className="small fw-semibold"),
                dbc.Select(
                    id="recomendacoes-filtro-cultura-safra", options=opcoes_cultura_safra(), placeholder="Todas"
                ),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("Região", className="small fw-semibold"),
                dbc.Select(id="recomendacoes-filtro-regiao", options=opcoes_regiao(), placeholder="Todas"),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("Linha de Produto", className="small fw-semibold"),
                dbc.Select(
                    id="recomendacoes-filtro-linha-produto", options=opcoes_linha_produto(), placeholder="Todas"
                ),
            ],
            md=2,
        ),
    ]
    return filter_card(filtros, button_id="recomendacoes-btn-filtrar")


def build_kpis(kpis: dict) -> dbc.Row:
    """Fileira de KPI cards do motor de recomendação."""
    cards = [
        kpi_card(
            "Recomendações Aceitas",
            format_percent(kpis["pct_aceitos"], with_sign=False),
            format_percent(kpis["pct_aceitos"], with_sign=False),
            0.0,
            "neutral",
        ),
        kpi_card(
            "Receita Incremental Estimada",
            format_currency(kpis["receita_incremental"]),
            format_currency(kpis["receita_incremental"]),
            0.0,
            "neutral",
        ),
        kpi_card(
            "Cobertura da Carteira",
            format_percent(kpis["cobertura_carteira"], with_sign=False),
            format_percent(kpis["cobertura_carteira"], with_sign=False),
            0.0,
            "neutral",
        ),
    ]
    return kpi_row(cards)


def build_chart_top_produtos(labels: list, values: list) -> dbc.Card:
    """Card com ranking de produtos mais recomendados no período."""
    fig = bar_ranking(labels, values, value_fmt=lambda v: f"{int(v)}", height=300)
    return card(
        "Produtos Mais Recomendados",
        dcc.Graph(id="recomendacoes-chart-top-produtos", figure=fig, config={"displayModeBar": False}),
    )


def build_grid(df: pd.DataFrame) -> dbc.Card:
    """
    Grid de recomendações por cliente. A coluna 'score' NÃO é recalculada aqui —
    RN-013 está needs_review (parsed:false) em docs/business_logic.yaml, sem
    fórmula/pesos declarados. Valor lido como veio de mock_data/recomendacoes.csv.
    """
    grid = data_table(
        df, id="recomendacoes-grid", numeric_cols=["score"], status_col="aceita"
    )
    return card(
        "Recomendações por Cliente",
        grid,
        right="score: RN-013 needs_review — sem fórmula de pesos declarada",
    )
