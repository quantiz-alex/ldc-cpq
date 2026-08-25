"""Callbacks da página Motor de Recomendação (Cross-sell)."""
from __future__ import annotations

from dash import Input, Output, State, callback, dcc, no_update

from frontend.pages.recomendacoes.recomendacoes_components import build_chart_top_produtos, build_grid, build_kpis
from frontend.pages.recomendacoes.recomendacoes_queries import calcular_kpis, carregar_recomendacoes, dados_grafico_top_produtos


def register_callbacks() -> None:
    """Registra todos os callbacks da página Motor de Recomendação."""

    # [Padrão 1] Filtrar grid, KPIs e gráfico — RN-014: RTV só vê sua carteira
    @callback(
        Output("recomendacoes-grid-col", "children"),
        Output("recomendacoes-kpis-row", "children"),
        Output("recomendacoes-chart-col", "children"),
        Input("recomendacoes-btn-filtrar", "n_clicks"),
        State("recomendacoes-filtro-cliente", "value"),
        State("recomendacoes-filtro-cultura-safra", "value"),
        State("recomendacoes-filtro-regiao", "value"),
        State("recomendacoes-filtro-linha-produto", "value"),
        State("current-user", "data"),
        prevent_initial_call=False,
    )
    def atualizar_recomendacoes(
        n_clicks: int,
        cliente: str | None,
        cultura_safra: str | None,
        regiao: str | None,
        linha_produto: str | None,
        user_data: dict | None,
    ) -> tuple:
        user_role = (user_data or {}).get("role")
        user_id = (user_data or {}).get("id")

        df = carregar_recomendacoes(
            cliente=cliente,
            cultura_safra=cultura_safra,
            regiao=regiao,
            linha_produto=linha_produto,
            user_role=user_role,
            user_id=user_id,
        )
        kpis = calcular_kpis(df)
        labels, values = dados_grafico_top_produtos(df)

        return build_grid(df), build_kpis(kpis), build_chart_top_produtos(labels, values)

    # [Padrão 6] Export Excel
    @callback(
        Output("recomendacoes-download-excel", "data"),
        Input("recomendacoes-btn-exportar", "n_clicks"),
        State("recomendacoes-filtro-cliente", "value"),
        State("current-user", "data"),
        prevent_initial_call=True,
    )
    def exportar_excel(n_clicks: int, cliente: str | None, user_data: dict | None):
        if not n_clicks:
            return no_update

        user_role = (user_data or {}).get("role")
        user_id = (user_data or {}).get("id")
        df = carregar_recomendacoes(cliente=cliente, user_role=user_role, user_id=user_id)

        return dcc.send_data_frame(
            df.to_excel, "recomendacoes_export.xlsx", sheet_name="Recomendacoes", index=False
        )
