"""Callbacks da página Relatórios Comerciais.

Exportação em PDF: fora do stack 100% Python/Dash não há geração nativa de PDF
sem biblioteca adicional (ex.: reportlab), proibida pelas regras deste projeto.
Implementado como fallback: gera o Excel e avisa o usuário via toast — ver aviso
no relatório final do frontend-builder.
"""
from __future__ import annotations

from dash import Input, Output, State, callback, dcc, no_update

from frontend.pages.relatorios.relatorios_components import build_chart_eficiencia, build_chart_receita, build_grid
from frontend.pages.relatorios.relatorios_queries import carregar_relatorio, dados_grafico_eficiencia, dados_grafico_receita_periodo


def register_callbacks() -> None:
    """Registra todos os callbacks da página Relatórios Comerciais."""

    # [Padrão 1] Filtrar relatório — RN-015: escopo por carteira/região do usuário
    @callback(
        Output("relatorios-grid-col", "children"),
        Output("relatorios-chart-receita-col", "children"),
        Output("relatorios-chart-eficiencia-col", "children"),
        Input("relatorios-btn-filtrar", "n_clicks"),
        State("relatorios-filtro-periodo", "start_date"),
        State("relatorios-filtro-periodo", "end_date"),
        State("relatorios-filtro-rtv", "value"),
        State("relatorios-filtro-regiao", "value"),
        State("relatorios-filtro-cliente", "value"),
        State("relatorios-filtro-linha-produto", "value"),
        State("current-user", "data"),
        prevent_initial_call=False,
    )
    def atualizar_relatorio(
        n_clicks: int,
        data_inicio: str | None,
        data_fim: str | None,
        rtv: str | None,
        regiao: str | None,
        cliente: str | None,
        linha_produto: str | None,
        user_data: dict | None,
    ) -> tuple:
        user_role = (user_data or {}).get("role")
        user_id = (user_data or {}).get("id")

        df = carregar_relatorio(
            data_inicio=data_inicio,
            data_fim=data_fim,
            rtv=rtv,
            regiao=regiao,
            cliente=cliente,
            linha_produto=linha_produto,
            user_role=user_role,
            user_id=user_id,
        )
        x, series = dados_grafico_receita_periodo(df)
        labels, values = dados_grafico_eficiencia(df)

        return build_grid(df), build_chart_receita(x, series), build_chart_eficiencia(labels, values)

    # [Padrão 6] Export Excel
    @callback(
        Output("relatorios-download-excel", "data"),
        Output("relatorios-toast", "is_open"),
        Output("relatorios-toast", "children"),
        Output("relatorios-toast", "color"),
        Input("relatorios-btn-exportar-excel", "n_clicks"),
        Input("relatorios-btn-exportar-pdf", "n_clicks"),
        State("relatorios-filtro-rtv", "value"),
        State("relatorios-filtro-regiao", "value"),
        State("current-user", "data"),
        prevent_initial_call=True,
    )
    def exportar(
        n_excel: int, n_pdf: int, rtv: str | None, regiao: str | None, user_data: dict | None
    ) -> tuple:
        from dash import ctx

        if not (n_excel or n_pdf):
            return no_update, False, "", "success"

        user_role = (user_data or {}).get("role")
        user_id = (user_data or {}).get("id")
        df = carregar_relatorio(rtv=rtv, regiao=regiao, user_role=user_role, user_id=user_id)

        arquivo = dcc.send_data_frame(
            df.to_excel, "relatorios_comerciais_export.xlsx", sheet_name="Relatorio", index=False
        )

        if ctx.triggered_id == "relatorios-btn-exportar-pdf":
            return (
                arquivo, True,
                "Exportação em PDF não disponível nesta versão (stack 100% Python/Dash) — "
                "arquivo gerado em Excel.",
                "warning",
            )
        return arquivo, True, "Relatório exportado em Excel.", "success"
