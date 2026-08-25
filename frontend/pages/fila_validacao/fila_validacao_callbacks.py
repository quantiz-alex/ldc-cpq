"""Callbacks da Fila de Validação do Trader (approval_queue) — skill-approval-flow.md."""
from __future__ import annotations

from dash import Input, Output, State, callback, ctx, dcc, no_update

from frontend.pages.fila_validacao.fila_validacao_components import build_grid, build_kpis
from frontend.pages.fila_validacao.fila_validacao_queries import (
    atualizar_status_aprovacao,
    calcular_kpis_fila,
    carregar_fila,
    obter_rtv_id,
)

TITULOS_ACAO = {
    "aprovar": "Aprovar",
    "rejeitar": "Rejeitar",
    "devolver": "Devolver com Questionamento",
}
STATUS_ACAO = {
    "aprovar": "Aprovado",
    "rejeitar": "Rejeitado",
    "devolver": "Devolvido",
}


def register_callbacks() -> None:
    """Registra todos os callbacks da Fila de Validação do Trader."""

    # ── Visibilidade por role (RN-007) ─────────────────────────────────────
    @callback(
        Output("fila-validacao-barra-aprovacao", "style"),
        Input("current-user", "data"),
        prevent_initial_call=False,
    )
    def controlar_visibilidade_aprovacao(user_data: dict | None) -> dict:
        if user_data and user_data.get("role") in ("trader", "admin"):
            return {"display": "flex", "alignItems": "center", "gap": "0.5rem"}
        return {"display": "none"}

    # [Padrão 1] Filtrar grid + KPIs
    @callback(
        Output("fila-validacao-grid-col", "children"),
        Output("fila-validacao-kpis-row", "children"),
        Input("fila-validacao-btn-filtrar", "n_clicks"),
        State("fila-validacao-filtro-status", "value"),
        State("fila-validacao-filtro-rtv", "value"),
        State("fila-validacao-filtro-com-alerta", "value"),
        State("fila-validacao-filtro-data-envio", "start_date"),
        State("fila-validacao-filtro-data-envio", "end_date"),
        prevent_initial_call=False,
    )
    def atualizar_fila(
        n_clicks: int,
        status: str | None,
        rtv: str | None,
        com_alerta: str | None,
        data_inicio: str | None,
        data_fim: str | None,
    ) -> tuple:
        df = carregar_fila(
            status=status,
            rtv=rtv,
            com_alerta=com_alerta,
            data_inicio=data_inicio,
            data_fim=data_fim,
            apenas_pendentes=not status,
        )
        kpis = calcular_kpis_fila()
        return build_grid(df), build_kpis(kpis)

    # ── Abrir modal de aprovação/rejeição/devolução ────────────────────────
    @callback(
        Output("fila-validacao-modal-aprovacao", "is_open"),
        Output("fila-validacao-modal-aprovacao-titulo", "children"),
        Output("fila-validacao-modal-aprovacao-descricao", "children"),
        Output("fila-validacao-hidden-acao-aprovacao", "data"),
        Output("fila-validacao-input-comentario-aprovacao", "value"),
        Input("fila-validacao-btn-aprovar", "n_clicks"),
        Input("fila-validacao-btn-rejeitar", "n_clicks"),
        Input("fila-validacao-btn-devolver", "n_clicks"),
        Input("fila-validacao-btn-cancelar-aprovacao", "n_clicks"),
        State("fila-validacao-grid", "selectedRows"),
        State("current-user", "data"),
        prevent_initial_call=True,
    )
    def toggle_modal_aprovacao(
        n_aprovar: int,
        n_rejeitar: int,
        n_devolver: int,
        n_cancelar: int,
        selected_rows: list,
        user_data: dict | None,
    ) -> tuple:
        triggered = ctx.triggered_id

        if triggered == "fila-validacao-btn-cancelar-aprovacao":
            return False, "", "", None, ""

        if not selected_rows:
            return False, "", "", None, ""

        # RN-009 — RTV não pode aprovar seus próprios pedidos
        user_id = (user_data or {}).get("id")
        autores = {obter_rtv_id(row["id"]) for row in selected_rows}
        if user_id in autores:
            return (
                False, "", "", None, "",
            )

        n = len(selected_rows)
        acao = {
            "fila-validacao-btn-aprovar": "aprovar",
            "fila-validacao-btn-rejeitar": "rejeitar",
            "fila-validacao-btn-devolver": "devolver",
        }.get(triggered)
        if acao is None:
            return False, "", "", None, ""

        return (
            True,
            f"{TITULOS_ACAO[acao]} {n} pedido(s)",
            f"Os {n} pedido(s) selecionados serão marcados como {STATUS_ACAO[acao]}.",
            acao,
            "",
        )

    # ── Confirmar aprovação/rejeição/devolução ─────────────────────────────
    @callback(
        Output("fila-validacao-grid-col", "children", allow_duplicate=True),
        Output("fila-validacao-kpis-row", "children", allow_duplicate=True),
        Output("fila-validacao-toast", "is_open", allow_duplicate=True),
        Output("fila-validacao-toast", "children", allow_duplicate=True),
        Output("fila-validacao-toast", "color", allow_duplicate=True),
        Output("fila-validacao-modal-aprovacao", "is_open", allow_duplicate=True),
        Input("fila-validacao-btn-confirmar-aprovacao", "n_clicks"),
        State("fila-validacao-hidden-acao-aprovacao", "data"),
        State("fila-validacao-grid", "selectedRows"),
        State("fila-validacao-input-comentario-aprovacao", "value"),
        State("current-user", "data"),
        prevent_initial_call=True,
    )
    def executar_aprovacao(
        n_clicks: int,
        acao: str | None,
        selected_rows: list,
        comentario: str | None,
        user_data: dict | None,
    ) -> tuple:
        if not n_clicks or not selected_rows or not acao:
            return no_update, no_update, False, "", "success", False

        # RN-008 — rejeição e devolução exigem comentário
        if acao in ("rejeitar", "devolver") and not comentario:
            return (
                no_update, no_update, True,
                "Informe o motivo antes de confirmar a rejeição/devolução (RN-008).",
                "warning", True,
            )

        # RN-009 — bloqueio redundante de auto-aprovação na confirmação
        user_id = (user_data or {}).get("id")
        autores = {obter_rtv_id(row["id"]) for row in selected_rows}
        if user_id in autores:
            return (
                no_update, no_update, True,
                "RTV não pode aprovar/rejeitar/devolver seus próprios pedidos (RN-009).",
                "danger", False,
            )

        ids = [row["id"] for row in selected_rows]
        avaliador = (user_data or {}).get("nome", "sistema")
        novo_status = STATUS_ACAO[acao]

        atualizados = atualizar_status_aprovacao(
            ids, novo_status, aprovado_por=avaliador, comentario=comentario
        )

        df = carregar_fila(apenas_pendentes=True)
        kpis = calcular_kpis_fila()
        msg = f"{atualizados} pedido(s) {novo_status.lower()}(s) com sucesso."
        cor = "success" if novo_status == "Aprovado" else "warning"
        return build_grid(df), build_kpis(kpis), True, msg, cor, False

    # [Padrão 6] Export Excel
    @callback(
        Output("fila-validacao-download-excel", "data"),
        Input("fila-validacao-btn-exportar", "n_clicks"),
        State("fila-validacao-filtro-status", "value"),
        State("fila-validacao-filtro-rtv", "value"),
        prevent_initial_call=True,
    )
    def exportar_excel(n_clicks: int, status: str | None, rtv: str | None):
        if not n_clicks:
            return no_update
        df = carregar_fila(status=status, rtv=rtv, apenas_pendentes=not status)
        return dcc.send_data_frame(
            df.to_excel, "fila_validacao_export.xlsx", sheet_name="Fila", index=False
        )
