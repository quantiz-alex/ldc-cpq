"""Callbacks da página de criação/edição de pedido (Captação de Pedido — CPQ).

Preço unitário/subtotal são SEMPRE calculados por RN-004 (preco_base do produto ×
% condição de pagamento × % janela/safra) em captacao_pedido_queries.py — nenhum
callback aqui aceita preço digitado.
"""
from __future__ import annotations

from dash import Input, Output, State, callback, ctx, no_update

from frontend.pages.captacao_pedido.captacao_pedido_components import build_grid_itens
from frontend.pages.captacao_pedido.captacao_pedido_queries import (
    adicionar_item,
    atualizar_cabecalho_pedido,
    carregar_itens_pedido,
    descartar_pedido,
    enviar_para_validacao,
)

_STORE = "captacao-pedido-store-pedido-ativo"
_ROTA_LISTAGEM = "/captacao-pedido"


def register_callbacks() -> None:
    """Registra todos os callbacks da página de pedido (Cabeçalho/Item/Itens)."""

    # ── Salvar Cabeçalho ───────────────────────────────────────────────────────
    @callback(
        Output("captacao-pedido-form-toast", "is_open", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "children", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "color", allow_duplicate=True),
        Input("captacao-pedido-btn-salvar-cabecalho", "n_clicks"),
        State(_STORE, "data"),
        State("captacao-pedido-form-cliente", "value"),
        State("captacao-pedido-form-cultura-safra", "value"),
        State("captacao-pedido-form-canal-origem", "value"),
        State("captacao-pedido-form-observacoes", "value"),
        prevent_initial_call=True,
    )
    def salvar_cabecalho(
        n_clicks: int,
        pedido_id: int | None,
        cliente_id,
        cultura_safra,
        canal_origem,
        observacoes,
    ):
        if not n_clicks:
            return False, "", "success"
        if pedido_id is None:
            return True, "Pedido inválido — volte para Meus Pedidos e tente novamente.", "warning"

        atualizar_cabecalho_pedido(
            pedido_id,
            cliente_id=cliente_id,
            cultura_safra=cultura_safra,
            canal_origem=canal_origem,
            observacoes=observacoes,
        )
        return True, "Cabeçalho do pedido salvo.", "success"

    # ── Adicionar Item — preço sempre calculado por RN-004, nunca digitado ────
    @callback(
        Output("captacao-pedido-grid-itens-col", "children", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "is_open", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "children", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "color", allow_duplicate=True),
        Input("captacao-pedido-btn-adicionar-item", "n_clicks"),
        State(_STORE, "data"),
        State("captacao-pedido-form-produto", "value"),
        State("captacao-pedido-form-quantidade", "value"),
        State("captacao-pedido-form-janela-mes", "value"),
        State("captacao-pedido-form-janela-ano", "value"),
        State("captacao-pedido-form-formato-entrega", "value"),
        State("captacao-pedido-form-condicao-pagamento", "value"),
        State("captacao-pedido-form-local-entrega", "value"),
        prevent_initial_call=True,
    )
    def adicionar_item_pedido(
        n_clicks: int,
        pedido_id: int | None,
        produto_id,
        quantidade,
        janela_mes,
        janela_ano,
        formato_entrega,
        condicao_pagamento,
        local_entrega,
    ):
        if not n_clicks:
            return no_update, False, "", "success"
        if pedido_id is None:
            return no_update, True, "Pedido inválido — volte para Meus Pedidos e tente novamente.", "warning"

        campos = [
            produto_id, quantidade, janela_mes, janela_ano,
            formato_entrega, condicao_pagamento, local_entrega,
        ]
        if any(c is None or c == "" for c in campos):
            return (
                no_update, True,
                "Preencha produto, quantidade, janela, formato de entrega, condição de "
                "pagamento e local de entrega antes de adicionar o item (RN-003).",
                "warning",
            )

        sucesso, mensagem = adicionar_item(
            pedido_id=pedido_id,
            produto_id=int(produto_id),
            quantidade=float(quantidade),
            janela_mes=int(janela_mes),
            janela_ano=int(janela_ano),
            formato_entrega=formato_entrega,
            condicao_pagamento=condicao_pagamento,
            local_entrega=local_entrega,
        )
        if not sucesso:
            return no_update, True, mensagem, "warning"

        df_itens = carregar_itens_pedido(pedido_id)
        return build_grid_itens(df_itens), True, mensagem, "success"

    # ── Enviar para Validação (Padrão 3) — some para a listagem quando aceito ──
    @callback(
        Output("captacao-pedido-form-toast", "is_open", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "children", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "color", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Input("captacao-pedido-btn-enviar-aprovacao", "n_clicks"),
        State(_STORE, "data"),
        prevent_initial_call=True,
    )
    def enviar_pedido_para_validacao(n_clicks: int, pedido_id: int | None):
        if not n_clicks:
            return False, "", "success", no_update
        if pedido_id is None:
            return True, "Pedido inválido — volte para Meus Pedidos e tente novamente.", "warning", no_update

        ok, mensagem = enviar_para_validacao(pedido_id)
        if ok:
            return True, mensagem, "success", _ROTA_LISTAGEM
        return True, mensagem, "warning", no_update

    # ── Voltar — abre a confirmação (salvar como rascunho ou descartar) ───────
    @callback(
        Output("captacao-pedido-modal-confirmar-saida", "is_open"),
        Input("captacao-pedido-form-btn-voltar", "n_clicks"),
        Input("captacao-pedido-form-btn-cancelar-saida", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_modal_confirmar_saida(n_voltar: int, n_cancelar: int) -> bool:
        return ctx.triggered_id == "captacao-pedido-form-btn-voltar"

    # ── Salvar como Rascunho — os dados já estão persistidos, só volta ────────
    @callback(
        Output("url", "pathname", allow_duplicate=True),
        Input("captacao-pedido-form-btn-salvar-rascunho", "n_clicks"),
        prevent_initial_call=True,
    )
    def salvar_como_rascunho_e_voltar(n_clicks: int):
        if not n_clicks:
            return no_update
        return _ROTA_LISTAGEM

    # ── Descartar Pedido — apaga o rascunho e seus itens, depois volta ────────
    @callback(
        Output("url", "pathname", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "is_open", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "children", allow_duplicate=True),
        Output("captacao-pedido-form-toast", "color", allow_duplicate=True),
        Input("captacao-pedido-form-btn-descartar", "n_clicks"),
        State(_STORE, "data"),
        prevent_initial_call=True,
    )
    def descartar_e_voltar(n_clicks: int, pedido_id: int | None):
        if not n_clicks:
            return no_update, False, "", "success"
        if pedido_id is None:
            return no_update, True, "Pedido inválido.", "warning"

        ok, mensagem = descartar_pedido(pedido_id)
        if ok:
            return _ROTA_LISTAGEM, no_update, no_update, no_update
        return no_update, True, mensagem, "warning"
