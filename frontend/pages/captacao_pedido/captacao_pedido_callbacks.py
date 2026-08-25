"""Callbacks da página Captação de Pedido (CPQ) — listagem "Meus Pedidos".

Nenhum callback de simulação/slider aqui — a precificação (RN-004) é uma fórmula
determinística (preco_base × % condição × % janela) recalculada em
captacao_pedido_queries.py a cada leitura da grid de itens, nunca um cálculo
ajustável por parâmetro do usuário.

Criação/edição de pedido (Cabeçalho, Adicionar Item, Itens do Pedido) vive em rota
própria — ver captacao_pedido_form_callbacks.py. Aqui só navegamos até lá, sempre
carregando o pedido pela query string (?pedido_id=N) para a página de destino já
nascer populada, sem depender de um callback de "população" que corresse contra a
troca de rota.
"""
from __future__ import annotations

from dash.exceptions import PreventUpdate

from dash import Input, Output, State, callback, ctx, no_update

from frontend.pages.captacao_pedido.captacao_pedido_components import build_grid_rascunhos
from frontend.pages.captacao_pedido.captacao_pedido_queries import (
    carregar_pedidos_em_aberto,
    criar_pedido_rascunho,
)

_ROTA_FORM = "/captacao-pedido/novo-pedido"


def register_callbacks() -> None:
    """Registra todos os callbacks da listagem de Captação de Pedido."""

    # [Padrão 1] Carregar/atualizar grid de pedidos em aberto do RTV logado — refaz
    # sempre que o usuário (re)visita a rota, inclusive ao voltar da página de pedido.
    @callback(
        Output("captacao-pedido-grid-rascunhos-col", "children"),
        Input("url", "pathname"),
        State("current-user", "data"),
        prevent_initial_call=False,
    )
    def atualizar_grid_rascunhos(pathname: str, user_data: dict | None):
        if pathname != "/captacao-pedido":
            raise PreventUpdate
        user_role = (user_data or {}).get("role")
        user_id = (user_data or {}).get("id")
        df = carregar_pedidos_em_aberto(user_role=user_role, user_id=user_id)
        return build_grid_rascunhos(df)

    # ── "Ver Detalhes" na grid de rascunhos → navega para a página de detalhes ────
    @callback(
        Output("url", "pathname", allow_duplicate=True),
        Output("url", "search", allow_duplicate=True),
        Input("captacao-pedido-grid-rascunhos", "cellClicked"),
        prevent_initial_call=True,
    )
    def selecionar_pedido_ativo(cell_clicked: dict):
        if not cell_clicked or cell_clicked.get("colId") != "acoes":
            return no_update, no_update
        pedido_id = cell_clicked.get("value")
        if pedido_id is None:
            return no_update, no_update
        return _ROTA_FORM, f"?pedido_id={int(pedido_id)}"

    # ── Novo Pedido — cria rascunho vazio e navega para a página de detalhes ──────
    @callback(
        Output("url", "pathname", allow_duplicate=True),
        Output("url", "search", allow_duplicate=True),
        Input("captacao-pedido-btn-novo", "n_clicks"),
        State("current-user", "data"),
        prevent_initial_call=True,
    )
    def criar_novo_pedido(n_clicks: int, user_data: dict | None):
        if not n_clicks or not user_data or not user_data.get("id"):
            return no_update, no_update

        pedido_id = criar_pedido_rascunho(
            cliente_id=None,  # type: ignore[arg-type]
            rtv_id=user_data["id"],
            cultura_safra=None,
            canal_origem="Manual",
        )
        return _ROTA_FORM, f"?pedido_id={pedido_id}"

    # ── Captura Assistida — abrir/fechar modal (RN-005) ────────────────────────
    @callback(
        Output("captacao-pedido-modal-captura-assistida", "is_open"),
        Input("captacao-pedido-btn-importar-mensagem", "n_clicks"),
        Input("captacao-pedido-btn-cancelar-captura", "n_clicks"),
        Input("captacao-pedido-btn-confirmar-captura", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_modal_captura(n_abrir: int, n_cancelar: int, n_confirmar: int) -> bool:
        return ctx.triggered_id == "captacao-pedido-btn-importar-mensagem"

    # ── Captura Assistida — confirmar geração de rascunho (RN-005) ────────────
    @callback(
        Output("url", "pathname", allow_duplicate=True),
        Output("url", "search", allow_duplicate=True),
        Output("captacao-pedido-toast", "is_open", allow_duplicate=True),
        Output("captacao-pedido-toast", "children", allow_duplicate=True),
        Output("captacao-pedido-toast", "color", allow_duplicate=True),
        Input("captacao-pedido-btn-confirmar-captura", "n_clicks"),
        State("captacao-pedido-captura-canal", "value"),
        State("captacao-pedido-captura-texto", "value"),
        State("current-user", "data"),
        prevent_initial_call=True,
    )
    def confirmar_captura_assistida(
        n_clicks: int, canal: str | None, texto: str | None, user_data: dict | None
    ):
        if not n_clicks:
            return no_update, no_update, False, "", "success"
        if not texto:
            return (
                no_update, no_update, True,
                "Cole o conteúdo da mensagem antes de gerar o rascunho.", "warning",
            )
        if not user_data or not user_data.get("id"):
            return no_update, no_update, True, "Faça login para gerar o rascunho.", "warning"

        pedido_id = criar_pedido_rascunho(
            cliente_id=None,  # type: ignore[arg-type]
            rtv_id=user_data["id"],
            cultura_safra=None,
            canal_origem=canal or "WhatsApp",
            observacoes=f"[Captura assistida] {texto}",
        )
        return _ROTA_FORM, f"?pedido_id={pedido_id}", no_update, no_update, no_update
