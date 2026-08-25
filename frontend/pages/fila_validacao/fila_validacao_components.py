"""Componentes visuais da Fila de Validação do Trader (approval_queue)."""
from __future__ import annotations

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html

from frontend.components.ui_components import filter_card, format_currency, format_number, kpi_card, kpi_row

from frontend.pages.fila_validacao.fila_validacao_queries import opcoes_rtv

STATUS_OPTIONS = [
    {"label": s, "value": s}
    for s in ["Pendente Aprovação", "Aprovado", "Rejeitado", "Devolvido"]
]
COM_ALERTA_OPTIONS = [{"label": "Sim", "value": "Sim"}, {"label": "Não", "value": "Não"}]

STATUS_BADGE_COLORS: dict[str, str] = {
    "Rascunho": "#6B7280",
    "Pendente Aprovação": "#B45309",
    "Aprovado": "#16A34A",
    "Rejeitado": "#DC2626",
    "Devolvido": "#DC2626",
}


def build_filtros() -> dbc.Card:
    """Card de filtros da fila (status, RTV, alerta, data de envio)."""
    filtros = [
        dbc.Col(
            [
                dbc.Label("Status", className="small fw-semibold"),
                dbc.Select(id="fila-validacao-filtro-status", options=STATUS_OPTIONS, placeholder="Todos"),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("RTV", className="small fw-semibold"),
                dbc.Select(id="fila-validacao-filtro-rtv", options=opcoes_rtv(), placeholder="Todos"),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("Com Alerta", className="small fw-semibold"),
                dbc.Select(
                    id="fila-validacao-filtro-com-alerta", options=COM_ALERTA_OPTIONS, placeholder="Todos"
                ),
            ],
            md=2,
        ),
        dbc.Col(
            [
                dbc.Label("Data de Envio", className="small fw-semibold"),
                dcc.DatePickerRange(
                    id="fila-validacao-filtro-data-envio", display_format="DD/MM/YYYY", className="d-block"
                ),
            ],
            md=3,
        ),
    ]
    return filter_card(filtros, button_id="fila-validacao-btn-filtrar")


def build_kpis(kpis: dict) -> dbc.Row:
    """Fileira de KPI cards da fila de validação."""
    cards = [
        kpi_card(
            "Pendentes",
            format_number(kpis["pendentes"]),
            format_number(kpis["pendentes"]),
            0.0,
            "neutral",
        ),
        kpi_card(
            "Aprovados Hoje",
            format_number(kpis["aprovados_hoje"]),
            format_number(kpis["aprovados_hoje"]),
            0.0,
            "neutral",
        ),
        kpi_card(
            "Rejeitados/Devolvidos Hoje",
            format_number(kpis["rejeitados_devolvidos_hoje"]),
            format_number(kpis["rejeitados_devolvidos_hoje"]),
            0.0,
            "neutral",
        ),
        kpi_card(
            "Tempo Médio de Validação",
            f"{kpis['tempo_medio_dias']:.1f} dias",
            f"{kpis['tempo_medio_dias']:.1f} dias",
            0.0,
            "neutral",
        ),
    ]
    return kpi_row(cards)


def get_status_column_def(field: str = "status") -> dict:
    """ColumnDef do AG Grid para status com badge colorido (skill-approval-flow.md)."""
    return {
        "field": field,
        "headerName": "Status",
        "width": 160,
        "cellStyle": {
            "function": (
                "params.value === 'Aprovado' ? {color: '#16A34A', fontWeight: '600'} : "
                "params.value === 'Rejeitado' ? {color: '#DC2626', fontWeight: '600'} : "
                "params.value === 'Devolvido' ? {color: '#DC2626', fontWeight: '600'} : "
                "params.value === 'Pendente Aprovação' ? {color: '#B45309', fontWeight: '600'} : "
                "{color: '#6B7280'}"
            )
        },
    }


def build_grid(df: pd.DataFrame) -> dbc.Card:
    """Grid de pedidos da fila com seleção múltipla para ações em lote."""
    column_defs = [
        {
            "headerCheckboxSelection": True,
            "checkboxSelection": True,
            "width": 50,
            "pinned": "left",
            "suppressMenu": True,
        },
        {"field": "id", "headerName": "ID", "width": 70},
        {"field": "cliente", "headerName": "Cliente", "flex": 1},
        {"field": "rtv", "headerName": "RTV", "flex": 1},
        {"field": "canal_origem", "headerName": "Canal", "width": 110},
        {
            "field": "valor_total",
            "headerName": "Valor Total",
            "type": "numericColumn",
            "valueFormatter": {"function": "d3.format(',.2f')(params.value)"},
            "cellStyle": {"fontFamily": "monospace"},
        },
        get_status_column_def(),
        {
            "field": "com_alerta",
            "headerName": "Alerta (RN-011)",
            "width": 130,
            "cellStyle": {
                "function": "params.value === 'Sim' ? {color: '#B45309', fontWeight: '600'} : {color: '#6B7280'}"
            },
        },
        {"field": "aprovado_por", "headerName": "Avaliado por", "flex": 1},
        {"field": "aprovado_em", "headerName": "Avaliado em", "flex": 1},
        {"field": "comentario_aprovacao", "headerName": "Comentário", "flex": 2},
    ]
    grid = dag.AgGrid(
        id="fila-validacao-grid",
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
            "rowSelection": "multiple",
            "suppressRowClickSelection": True,
            "animateRows": True,
        },
        className="ag-theme-alpine",
        style={"height": "500px"},
        csvExportParams={"fileName": "fila_validacao_export.csv"},
    )
    return dbc.Card(
        [
            dbc.CardHeader("Pedidos na Fila", className="bg-white border-bottom fw-semibold"),
            dbc.CardBody(grid, className="p-0"),
        ],
        className="shadow-sm border-0 mb-3",
    )


def build_barra_aprovacao() -> html.Div:
    """
    Barra de ações — visível apenas para trader/admin (RN-007), controlada via
    callback ligado a dcc.Store('current-user'). Inclui Aprovar, Rejeitar e
    Devolver com Questionamento (RN-008/009/010/011).
    """
    return html.Div(
        [
            dbc.Button(
                [html.I(className="bi bi-check-circle me-2"), "Aprovar"],
                id="fila-validacao-btn-aprovar",
                color="success",
                size="sm",
                className="me-2",
            ),
            dbc.Button(
                [html.I(className="bi bi-x-circle me-2"), "Rejeitar"],
                id="fila-validacao-btn-rejeitar",
                color="danger",
                size="sm",
                outline=True,
                className="me-2",
            ),
            dbc.Button(
                [html.I(className="bi bi-arrow-return-left me-2"), "Devolver com Questionamento"],
                id="fila-validacao-btn-devolver",
                color="warning",
                size="sm",
                outline=True,
            ),
        ],
        id="fila-validacao-barra-aprovacao",
        className="d-flex align-items-center gap-2 mb-3",
        style={"display": "none"},
    )


def build_modal_aprovacao() -> dbc.Modal:
    """Modal de aprovação/rejeição/devolução com comentário (RN-008)."""
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(id="fila-validacao-modal-aprovacao-titulo"), close_button=True),
            dbc.ModalBody(
                [
                    html.P(id="fila-validacao-modal-aprovacao-descricao", className="text-muted small mb-3"),
                    dbc.Label("Comentário", className="fw-semibold small"),
                    dbc.Textarea(
                        id="fila-validacao-input-comentario-aprovacao",
                        placeholder="Opcional para aprovação. Obrigatório para rejeição/devolução (RN-008).",
                        rows=3,
                    ),
                    dbc.FormText(
                        "Rejeições e devoluções exigem comentário explicando o motivo.", color="muted"
                    ),
                ]
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Cancelar",
                        id="fila-validacao-btn-cancelar-aprovacao",
                        color="secondary",
                        outline=True,
                        className="me-2",
                    ),
                    dbc.Button("Confirmar", id="fila-validacao-btn-confirmar-aprovacao", color="primary"),
                ]
            ),
            dcc.Store(id="fila-validacao-hidden-acao-aprovacao"),
        ],
        id="fila-validacao-modal-aprovacao",
        is_open=False,
        centered=True,
    )
