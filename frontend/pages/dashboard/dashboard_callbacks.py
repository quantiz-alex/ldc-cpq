"""Callbacks da página Dashboard Comercial."""
from __future__ import annotations

from dash import Input, Output, State, callback, dcc, no_update

from frontend.pages.dashboard.dashboard_components import build_chart_receita, build_chart_top_rtv, build_kpis
from frontend.pages.dashboard.dashboard_queries import (
    calcular_kpis,
    carregar_pedidos,
    dados_grafico_receita_semana,
    dados_grafico_top_rtv,
)


def register_callbacks() -> None:
    """Registra todos os callbacks da página Dashboard Comercial."""

    # [Padrão 1] Filtrar KPIs e gráficos — RN-001: RTV só vê a própria carteira
    @callback(
        Output("dashboard-kpis-row", "children"),
        Output("dashboard-chart-receita-col", "children"),
        Output("dashboard-chart-top-rtv-col", "children"),
        Input("dashboard-btn-filtrar", "n_clicks"),
        State("dashboard-filtro-periodo", "start_date"),
        State("dashboard-filtro-periodo", "end_date"),
        State("dashboard-filtro-rtv", "value"),
        State("dashboard-filtro-regiao", "value"),
        State("dashboard-filtro-linha-produto", "value"),
        State("dashboard-filtro-status", "value"),
        State("current-user", "data"),
        prevent_initial_call=False,
    )
    def atualizar_dashboard(
        n_clicks: int,
        data_inicio: str | None,
        data_fim: str | None,
        rtv: str | None,
        regiao: str | None,
        linha_produto: str | None,
        status: str | None,
        user_data: dict | None,
    ) -> tuple:
        user_role = (user_data or {}).get("role")
        user_id = (user_data or {}).get("id")

        df = carregar_pedidos(
            data_inicio=data_inicio,
            data_fim=data_fim,
            rtv=rtv,
            regiao=regiao,
            linha_produto=linha_produto,
            status=status,
            user_role=user_role,
            user_id=user_id,
        )

        kpis = calcular_kpis(df)
        x, series = dados_grafico_receita_semana(df)
        labels, values = dados_grafico_top_rtv(df)

        return (
            build_kpis(kpis),
            build_chart_receita(x, series),
            build_chart_top_rtv(labels, values),
        )

    # [Padrão 6] Export Excel
    @callback(
        Output("dashboard-download-excel", "data"),
        Input("dashboard-btn-exportar", "n_clicks"),
        State("dashboard-filtro-rtv", "value"),
        State("dashboard-filtro-regiao", "value"),
        State("current-user", "data"),
        prevent_initial_call=True,
    )
    def exportar_excel(
        n_clicks: int, rtv: str | None, regiao: str | None, user_data: dict | None
    ):
        if not n_clicks:
            return no_update

        user_role = (user_data or {}).get("role")
        user_id = (user_data or {}).get("id")
        df = carregar_pedidos(rtv=rtv, regiao=regiao, user_role=user_role, user_id=user_id)

        return dcc.send_data_frame(
            df.to_excel, "dashboard_comercial_export.xlsx", sheet_name="Pedidos", index=False
        )
