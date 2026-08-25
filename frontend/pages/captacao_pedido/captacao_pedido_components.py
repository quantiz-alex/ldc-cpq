"""Componentes visuais da Captação de Pedido (CPQ)."""
from __future__ import annotations

from typing import Any

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html

from frontend.components.ui_components import card

from frontend.pages.captacao_pedido.captacao_pedido_queries import (
    opcoes_clientes,
    opcoes_condicao_pagamento,
    opcoes_produtos,
)

CANAL_ORIGEM_OPTIONS = [
    {"label": "WhatsApp", "value": "WhatsApp"},
    {"label": "E-mail", "value": "Email"},
    {"label": "Imagem", "value": "Imagem"},
    {"label": "Manual", "value": "Manual"},
]

FORMATO_ENTREGA_OPTIONS = [
    {"label": "CIF", "value": "CIF"},
    {"label": "FOB", "value": "FOB"},
    {"label": "Entrega Programada", "value": "Entrega Programada"},
]


def build_grid_rascunhos(df: pd.DataFrame) -> dbc.Card:
    """Grid de pedidos em aberto (Rascunho/Pendente Aprovação/Devolvido) do RTV logado.

    Coluna "Ações" com "Ver Detalhes" — clicar nela (e só nela) navega para a página
    de edição do pedido. O cellClicked do dash-ag-grid só traz {value, colId, rowIndex,
    rowId, timestamp} — NÃO tem rowData — então a coluna reaproveita o campo "id" (o
    valueFormatter só troca a exibição para "Ver Detalhes") com colId explícito
    "acoes", para o callback usar cellClicked["value"] como o id do pedido clicado.
    """
    column_defs = [
        {"field": "id", "headerName": "ID", "width": 70},
        {"field": "cliente", "headerName": "Cliente", "flex": 1},
        {"field": "cultura_safra", "headerName": "Cultura/Safra", "flex": 1},
        {"field": "canal_origem", "headerName": "Canal", "width": 110},
        {
            "field": "valor_total",
            "headerName": "Valor Total",
            "type": "numericColumn",
            "valueFormatter": {"function": "d3.format(',.2f')(params.value)"},
            "cellStyle": {"fontFamily": "monospace"},
        },
        {"field": "status", "headerName": "Status", "width": 160},
        {
            "field": "id",
            "colId": "acoes",
            "headerName": "Ações",
            "width": 150,
            "sortable": False,
            "filter": False,
            "floatingFilter": False,
            "valueFormatter": {"function": "'🔍 Ver Detalhes'"},
            "cellStyle": {
                "color": "#1045C8",
                "fontWeight": "600",
                "cursor": "pointer",
                "textDecoration": "underline",
            },
        },
    ]

    grid = dag.AgGrid(
        id="captacao-pedido-grid-rascunhos",
        rowData=df.to_dict("records"),
        columnDefs=column_defs,
        defaultColDef={
            "sortable": True,
            "filter": True,
            "resizable": True,
            "floatingFilter": True,
            "suppressMenu": True,
        },
        dashGridOptions={
            "pagination": True,
            "paginationPageSize": 20,
            "paginationPageSizeSelector": [10, 20, 50, 100],
            "rowHeight": 44,
            "headerHeight": 44,
            "rowSelection": "single",
        },
        className="ag-theme-alpine",
        style={"height": "400px"},
    )
    return card("Meus Pedidos (Rascunho / Pendente / Devolvido)", grid)


def build_form_cabecalho(valores: dict | None = None) -> dbc.Card:
    """Formulário de cabeçalho do pedido — cliente, cultura/safra, canal, observações.

    `valores`, quando informado (ver detalhes de um pedido existente), pré-preenche os
    campos sem depender de um callback de população à parte — evita corrida entre a
    troca de rota e o preenchimento do formulário.
    """
    valores = valores or {}
    body = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Cliente *", className="small fw-semibold"),
                    dbc.Select(
                        id="captacao-pedido-form-cliente",
                        options=opcoes_clientes(),
                        value=valores.get("cliente_id"),
                        placeholder="Selecione o cliente",
                    ),
                ],
                md=4,
            ),
            dbc.Col(
                [
                    dbc.Label("Cultura/Safra", className="small fw-semibold"),
                    dbc.Input(
                        id="captacao-pedido-form-cultura-safra",
                        type="text",
                        value=valores.get("cultura_safra"),
                    ),
                ],
                md=3,
            ),
            dbc.Col(
                [
                    dbc.Label("Canal de Origem *", className="small fw-semibold"),
                    dbc.Select(
                        id="captacao-pedido-form-canal-origem",
                        options=CANAL_ORIGEM_OPTIONS,
                        value=valores.get("canal_origem") or "Manual",
                    ),
                ],
                md=3,
            ),
            dbc.Col(
                dbc.Button(
                    "Salvar Cabeçalho",
                    id="captacao-pedido-btn-salvar-cabecalho",
                    color="primary",
                    className="w-100 fw-bold",
                ),
                md=2,
                className="d-grid align-self-end",
            ),
            dbc.Col(
                [
                    dbc.Label("Observações", className="small fw-semibold"),
                    dbc.Textarea(
                        id="captacao-pedido-form-observacoes",
                        rows=2,
                        value=valores.get("observacoes"),
                    ),
                ],
                md=12,
                className="mt-2",
            ),
        ],
        className="g-2",
    )
    return card("Cabeçalho do Pedido", body)


def build_grid_itens(df: pd.DataFrame) -> dbc.Card:
    """
    Grid de itens do pedido. preco_unitario e subtotal são colunas computed
    (compute_from: RN-004) — sempre calculadas em captacao_pedido_queries.py via
    calculadas por fórmula (RN-004), nunca editáveis manualmente.
    """
    column_defs = [
        {"field": "id", "headerName": "ID", "width": 70},
        {"field": "produto_id", "headerName": "Produto ID", "width": 100},
        {"field": "nome_comercial", "headerName": "Produto", "flex": 1},
        {
            "field": "quantidade",
            "headerName": "Quantidade",
            "type": "numericColumn",
            "cellStyle": {"fontFamily": "monospace"},
        },
        {"field": "unidade", "headerName": "Un.", "width": 70},
        {"field": "janela_mes", "headerName": "Mês", "width": 80},
        {"field": "janela_ano", "headerName": "Ano", "width": 90},
        {"field": "formato_entrega", "headerName": "Formato Entrega"},
        {"field": "condicao_pagamento", "headerName": "Condição Pagamento"},
        {"field": "local_entrega", "headerName": "Local Entrega", "flex": 1},
        {
            "field": "preco_unitario",
            "headerName": "Preço Unitário (RN-004)",
            "type": "numericColumn",
            "valueFormatter": {
                "function": "params.value == null ? 'sem preço' : d3.format(',.2f')(params.value)"
            },
            "cellStyle": {
                "fontFamily": "monospace",
                "backgroundColor": "#f8fafc",
                "fontWeight": "600",
            },
            "editable": False,
        },
        {
            "field": "subtotal",
            "headerName": "Subtotal",
            "type": "numericColumn",
            "valueFormatter": {
                "function": "params.value == null ? 'sem preço' : d3.format(',.2f')(params.value)"
            },
            "cellStyle": {"fontFamily": "monospace", "fontWeight": "600"},
            "editable": False,
        },
    ]

    grid = dag.AgGrid(
        id="captacao-pedido-grid-itens",
        rowData=df.to_dict("records"),
        columnDefs=column_defs,
        defaultColDef={
            "sortable": True,
            "filter": True,
            "resizable": True,
            "floatingFilter": True,
            "suppressMenu": True,
        },
        dashGridOptions={
            "pagination": True,
            "paginationPageSize": 20,
            "rowHeight": 44,
            "headerHeight": 44,
            "rowSelection": "single",
        },
        className="ag-theme-alpine",
        style={"height": "360px"},
    )
    return card(
        "Itens do Pedido — preço automático por janela/condição (RN-004)",
        grid,
        right="Preço = preco_base × % condição × % janela",
    )


def build_form_item() -> dbc.Card:
    """Formulário de inclusão de item — o preço NUNCA é digitado manualmente (RN-004)."""
    body = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Produto *", className="small fw-semibold"),
                    dbc.Select(id="captacao-pedido-form-produto", options=opcoes_produtos()),
                ],
                md=3,
            ),
            dbc.Col(
                [
                    dbc.Label("Quantidade *", className="small fw-semibold"),
                    dbc.Input(id="captacao-pedido-form-quantidade", type="number", min=0),
                ],
                md=2,
            ),
            dbc.Col(
                [
                    dbc.Label("Mês Janela *", className="small fw-semibold"),
                    dbc.Input(id="captacao-pedido-form-janela-mes", type="number", min=1, max=12),
                ],
                md=1,
            ),
            dbc.Col(
                [
                    dbc.Label("Ano Janela *", className="small fw-semibold"),
                    dbc.Input(id="captacao-pedido-form-janela-ano", type="number", min=2024),
                ],
                md=2,
            ),
            dbc.Col(
                [
                    dbc.Label("Formato Entrega *", className="small fw-semibold"),
                    dbc.Select(
                        id="captacao-pedido-form-formato-entrega",
                        options=FORMATO_ENTREGA_OPTIONS,
                    ),
                ],
                md=2,
            ),
            dbc.Col(
                [
                    dbc.Label("Condição Pagto *", className="small fw-semibold"),
                    dbc.Select(
                        id="captacao-pedido-form-condicao-pagamento",
                        options=opcoes_condicao_pagamento(),
                    ),
                ],
                md=2,
            ),
            dbc.Col(
                [
                    dbc.Label("Local de Entrega *", className="small fw-semibold"),
                    dbc.Input(id="captacao-pedido-form-local-entrega", type="text"),
                ],
                md=8,
                className="mt-2",
            ),
            dbc.Col(
                dbc.Button(
                    "Adicionar Item",
                    id="captacao-pedido-btn-adicionar-item",
                    color="primary",
                    outline=True,
                    className="w-100 fw-bold mt-2",
                ),
                md=4,
                className="d-grid",
            ),
        ],
        className="g-2 align-items-end",
    )
    return card("Adicionar Item ao Pedido", body)


def build_modal_confirmar_saida() -> dbc.Modal:
    """Confirmação ao clicar em "Voltar" na página de pedido — salvar como rascunho
    (os dados já estão persistidos a cada ação) ou descartar o pedido inteiro."""
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Sair do pedido"), close_button=True),
            dbc.ModalBody(
                "O que deseja fazer com este pedido antes de voltar para Meus Pedidos?"
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Cancelar",
                        id="captacao-pedido-form-btn-cancelar-saida",
                        color="secondary",
                        outline=True,
                        className="me-auto",
                    ),
                    dbc.Button(
                        "Descartar Pedido",
                        id="captacao-pedido-form-btn-descartar",
                        color="danger",
                        outline=True,
                        className="me-2",
                    ),
                    dbc.Button(
                        "Salvar como Rascunho",
                        id="captacao-pedido-form-btn-salvar-rascunho",
                        color="primary",
                    ),
                ]
            ),
        ],
        id="captacao-pedido-modal-confirmar-saida",
        is_open=False,
        centered=True,
    )


def build_modal_captura_assistida() -> dbc.Modal:
    """RN-005 — captura assistida sempre gera Rascunho, exige revisão do RTV."""
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Captura Assistida por Mensagem"), close_button=True),
            dbc.ModalBody(
                [
                    html.P(
                        "Cole o texto da mensagem (WhatsApp/e-mail) recebida do cliente. "
                        "O sistema gera um rascunho para sua revisão — nunca cria pedido "
                        "diretamente (RN-005).",
                        className="text-muted small",
                    ),
                    dbc.Label("Canal *", className="small fw-semibold"),
                    dbc.Select(
                        id="captacao-pedido-captura-canal", options=CANAL_ORIGEM_OPTIONS, value="WhatsApp"
                    ),
                    dbc.Label("Conteúdo da Mensagem *", className="small fw-semibold mt-2"),
                    dbc.Textarea(id="captacao-pedido-captura-texto", rows=5),
                ]
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Cancelar",
                        id="captacao-pedido-btn-cancelar-captura",
                        color="secondary",
                        outline=True,
                        className="me-2",
                    ),
                    dbc.Button(
                        "Gerar Rascunho",
                        id="captacao-pedido-btn-confirmar-captura",
                        color="primary",
                    ),
                ]
            ),
        ],
        id="captacao-pedido-modal-captura-assistida",
        is_open=False,
        centered=True,
    )
