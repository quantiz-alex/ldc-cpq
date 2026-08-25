"""Consultas e regras de dados da Captação de Pedido (CPQ) — leitura via mock_data/*.csv.

IMPORTANTE — RN-004: o preço unitário é SEMPRE função de produto + janela de entrega +
condição comercial, calculado por fórmula (preco_base do produto × % fixo por condição
de pagamento × % fixo por janela/safra) — não é uma tabela de preços pré-cadastrada por
combinação, para garantir que todo produto ativo sempre tenha preço. Esta tela NÃO é uma
simulação — docs/business_logic.yaml não tem nenhuma regra logic_type:
interactive_formula vinculada ao módulo "Captação de Pedido (CPQ)": os percentuais são
parâmetros fixos, não ajustáveis pelo RTV. preco_unitario/subtotal são SEMPRE
recalculados por pandas a partir dessa fórmula, nunca lidos prontos de pedido_itens.csv
(mesmo que o mock já tenha essas colunas persistidas).
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent.parent / "mock_data"

_PEDIDOS_CSV = DATA_DIR / "pedidos.csv"
_ITENS_CSV = DATA_DIR / "pedido_itens.csv"
_CLIENTES_CSV = DATA_DIR / "clientes.csv"
_PRODUTOS_CSV = DATA_DIR / "produtos.csv"

STATUS_ABERTOS = ["Rascunho", "Pendente Aprovação", "Devolvido"]

# RN-004 — percentual fixo por condição de pagamento sobre o preço base do produto
# (custo de financiamento crescente por prazo; parâmetro travado, não editável pelo RTV).
CONDICAO_PAGAMENTO_PCT: dict[str, float] = {
    "À vista": 0.0,
    "30 dias": 0.04,
    "60 dias": 0.07,
    "90 dias": 0.11,
}

# RN-004 — percentual fixo por mês da janela de entrega: pico de safra (plantio da
# safra de verão em set/out/nov e da safrinha em fev/mar/abr) custa +5%; entressafra
# fica no preço base.
_MESES_PICO_SAFRA = {2, 3, 4, 9, 10, 11}
_PCT_JANELA_PICO_SAFRA = 0.05


def _pct_janela(janela_mes: int) -> float:
    return _PCT_JANELA_PICO_SAFRA if janela_mes in _MESES_PICO_SAFRA else 0.0


# ============================================================================
# LEITURA
# ============================================================================


def carregar_pedidos_em_aberto(
    user_role: str | None = None, user_id: int | None = None
) -> pd.DataFrame:
    """Pedidos ainda não aprovados/rejeitados do RTV logado (ou todos, para trader/admin)."""
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    clientes = pd.read_csv(_CLIENTES_CSV)

    df = pedidos[pedidos["status"].isin(STATUS_ABERTOS)].copy()
    if user_role == "rtv" and user_id is not None:
        df = df[df["rtv_id"] == user_id]

    df = df.merge(
        clientes[["id", "nome"]].rename(columns={"id": "cliente_id", "nome": "cliente_nome"}),
        on="cliente_id",
        how="left",
    )
    colunas = [
        "id",
        "cliente_nome",
        "cultura_safra",
        "canal_origem",
        "valor_total",
        "status",
    ]
    return df[colunas].rename(columns={"cliente_nome": "cliente"})


def _lookup_preco(
    produto_id: int,
    janela_mes: int,
    janela_ano: int,
    condicao_pagamento: str,
) -> float | None:
    """RN-004 — preco_base do produto × (1 + % da condição de pagamento) × (1 + %
    da janela/safra). janela_ano não afeta o valor (só a condição e o mês pesam),
    mas segue recebido para manter a assinatura estável e a vigência auditável."""
    produtos = pd.read_csv(_PRODUTOS_CSV)
    produto = produtos[produtos["id"] == produto_id]
    if produto.empty:
        return None

    preco_base = produto.iloc[0].get("preco_base")
    if pd.isna(preco_base):
        return None

    pct_condicao = CONDICAO_PAGAMENTO_PCT.get(condicao_pagamento)
    if pct_condicao is None:
        return None

    preco = float(preco_base) * (1 + pct_condicao) * (1 + _pct_janela(janela_mes))
    return round(preco, 2)


def carregar_cabecalho_pedido(pedido_id: int) -> dict:
    """Campos de cabeçalho de um pedido específico — usado para preencher o modal
    ao reabrir um pedido existente (ver detalhes)."""
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    pedido = pedidos[pedidos["id"] == pedido_id]
    if pedido.empty:
        return {}

    row = pedido.iloc[0]
    return {
        "cliente_id": None if pd.isna(row["cliente_id"]) else int(row["cliente_id"]),
        "cultura_safra": None if pd.isna(row["cultura_safra"]) else row["cultura_safra"],
        "canal_origem": None if pd.isna(row["canal_origem"]) else row["canal_origem"],
        "observacoes": None if pd.isna(row["observacoes"]) else row["observacoes"],
    }


def carregar_itens_pedido(pedido_id: int) -> pd.DataFrame:
    """
    Itens do pedido com preco_unitario/subtotal recalculados via RN-004 (fórmula:
    preco_base do produto × % condição de pagamento × % janela/safra). As colunas
    preco_unitario/subtotal já presentes em pedido_itens.csv são DESCARTADAS e
    recalculadas em pandas — nunca reaproveitadas diretamente do CSV, para garantir
    que a tela reflita sempre o preço vigente.
    """
    itens = pd.read_csv(_ITENS_CSV)
    itens = itens[itens["pedido_id"] == pedido_id].copy()
    if itens.empty:
        return itens.assign(preco_unitario=[], subtotal=[])

    produtos = pd.read_csv(_PRODUTOS_CSV)
    itens = itens.merge(
        produtos[["id", "nome_comercial"]].rename(columns={"id": "produto_id"}),
        on="produto_id",
        how="left",
    )

    precos_calc: list[float | None] = []
    subtotais: list[float | None] = []
    for _, item in itens.iterrows():
        preco = _lookup_preco(
            produto_id=int(item["produto_id"]),
            janela_mes=int(item["janela_mes"]),
            janela_ano=int(item["janela_ano"]),
            condicao_pagamento=str(item["condicao_pagamento"]),
        )
        precos_calc.append(preco)
        subtotais.append(round(preco * float(item["quantidade"]), 2) if preco is not None else None)

    itens["preco_unitario"] = precos_calc
    itens["subtotal"] = subtotais

    colunas = [
        "id",
        "produto_id",
        "nome_comercial",
        "quantidade",
        "unidade",
        "janela_mes",
        "janela_ano",
        "formato_entrega",
        "condicao_pagamento",
        "local_entrega",
        "preco_unitario",
        "subtotal",
    ]
    return itens[colunas]


def opcoes_clientes() -> list[dict]:
    """Opções de cliente para selects (form de cabeçalho)."""
    clientes = pd.read_csv(_CLIENTES_CSV)
    ativos = clientes[clientes["ativo"] == 1]
    return [{"label": row["nome"], "value": int(row["id"])} for _, row in ativos.iterrows()]


def opcoes_produtos() -> list[dict]:
    """Opções de produto para selects (grid de itens)."""
    produtos = pd.read_csv(_PRODUTOS_CSV)
    ativos = produtos[produtos["ativo"] == 1]
    return [
        {"label": row["nome_comercial"], "value": int(row["id"])} for _, row in ativos.iterrows()
    ]


def opcoes_condicao_pagamento() -> list[dict]:
    """Condições comerciais disponíveis (RN-004 — mesmas chaves de CONDICAO_PAGAMENTO_PCT)."""
    return [{"label": c, "value": c} for c in CONDICAO_PAGAMENTO_PCT]


# ============================================================================
# ESCRITA (mock — reescreve o CSV completo)
# ============================================================================


def criar_pedido_rascunho(
    cliente_id: int,
    rtv_id: int,
    cultura_safra: str | None,
    canal_origem: str,
    observacoes: str | None = None,
) -> int:
    """RN-005 — captura sempre grava em Rascunho, mesmo via captura assistida."""
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    novo_id = int(pedidos["id"].max()) + 1 if not pedidos.empty else 1
    agora = datetime.now().isoformat(timespec="seconds")

    nova_linha = {
        "id": novo_id,
        "cliente_id": cliente_id,
        "rtv_id": rtv_id,
        "cultura_safra": cultura_safra,
        "canal_origem": canal_origem,
        "valor_total": 0.0,
        "observacoes": observacoes,
        "status": "Rascunho",
        "aprovado_por": None,
        "aprovado_em": None,
        "comentario_aprovacao": None,
        "created_at": agora,
        "updated_at": agora,
    }
    pedidos = pd.concat([pedidos, pd.DataFrame([nova_linha])], ignore_index=True)
    pedidos.to_csv(_PEDIDOS_CSV, index=False)
    return novo_id


def atualizar_cabecalho_pedido(
    pedido_id: int,
    cliente_id: int | None,
    cultura_safra: str | None,
    canal_origem: str | None,
    observacoes: str | None,
) -> None:
    """Atualiza os campos de cabeçalho de um pedido em Rascunho."""
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    mascara = pedidos["id"] == pedido_id
    if cliente_id is not None:
        # dbc.Select sempre entrega "value" como string, mesmo com options int —
        # cliente_id é float64 no CSV (NaN em pedidos sem cliente), então uma
        # string quebraria o setitem do pandas 2.x (LossySetitemError).
        pedidos.loc[mascara, "cliente_id"] = int(cliente_id)
    if cultura_safra is not None:
        pedidos.loc[mascara, "cultura_safra"] = cultura_safra
    if canal_origem is not None:
        pedidos.loc[mascara, "canal_origem"] = canal_origem
    if observacoes is not None:
        pedidos.loc[mascara, "observacoes"] = observacoes
    pedidos.loc[mascara, "updated_at"] = datetime.now().isoformat(timespec="seconds")
    pedidos.to_csv(_PEDIDOS_CSV, index=False)


def validar_pedido_completo(pedido_id: int) -> tuple[bool, str]:
    """RN-003 — valida completude antes de permitir o envio para validação."""
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    pedido = pedidos[pedidos["id"] == pedido_id]
    if pedido.empty:
        return False, "Pedido não encontrado."
    if pd.isna(pedido.iloc[0]["cliente_id"]):
        return False, "Selecione um cliente antes de enviar para validação."

    itens = pd.read_csv(_ITENS_CSV)
    itens_pedido = itens[itens["pedido_id"] == pedido_id]
    if itens_pedido.empty:
        return False, "Adicione ao menos um item antes de enviar para validação."

    campos_obrigatorios = [
        "quantidade",
        "janela_mes",
        "janela_ano",
        "formato_entrega",
        "condicao_pagamento",
        "local_entrega",
    ]
    for campo in campos_obrigatorios:
        if itens_pedido[campo].isna().any():
            return (
                False,
                "Pedido incompleto — preencha cliente, ao menos 1 item, quantidade, "
                "janela de entrega, formato de entrega, prazo de pagamento e local de "
                "entrega antes de enviar para validação.",
            )
    return True, ""


def adicionar_item(
    pedido_id: int,
    produto_id: int,
    quantidade: float,
    janela_mes: int,
    janela_ano: int,
    formato_entrega: str,
    condicao_pagamento: str,
    local_entrega: str,
    unidade: str = "un",
) -> tuple[bool, str]:
    """
    Adiciona item ao pedido. preco_unitario/subtotal são persistidos apenas como
    snapshot inicial (RN-004 os recalcula sempre na leitura via carregar_itens_pedido —
    a tela nunca exibe o valor persistido sem reconferir o cálculo vigente).

    RN-004 exige preço calculado por fórmula (preco_base × % condição × % janela) — se
    o produto não tiver preco_base cadastrado ou a condição de pagamento for inválida,
    o item NÃO é gravado (nunca persiste um preço 0.0 fantasma).
    """
    preco = _lookup_preco(produto_id, janela_mes, janela_ano, condicao_pagamento)
    if preco is None:
        return False, (
            "Não foi possível calcular o preço (RN-004) — verifique se o produto tem "
            "preço base cadastrado e se a condição de pagamento é válida."
        )

    itens = pd.read_csv(_ITENS_CSV)
    novo_id = int(itens["id"].max()) + 1 if not itens.empty else 1
    agora = datetime.now().isoformat(timespec="seconds")
    subtotal = round(preco * float(quantidade), 2)

    nova_linha = {
        "id": novo_id,
        "pedido_id": pedido_id,
        "produto_id": produto_id,
        "quantidade": quantidade,
        "unidade": unidade,
        "janela_mes": janela_mes,
        "janela_ano": janela_ano,
        "formato_entrega": formato_entrega,
        "local_entrega": local_entrega,
        "condicao_pagamento": condicao_pagamento,
        "preco_unitario": preco,
        "subtotal": subtotal,
        "created_at": agora,
        "updated_at": agora,
    }
    itens = pd.concat([itens, pd.DataFrame([nova_linha])], ignore_index=True)
    itens.to_csv(_ITENS_CSV, index=False)
    _recalcular_valor_total(pedido_id)
    return True, "Item adicionado — preço calculado por RN-004."


def descartar_pedido(pedido_id: int) -> tuple[bool, str]:
    """Remove definitivamente um pedido em Rascunho e seus itens — ação de "Voltar"
    escolhendo descartar em vez de salvar. Só permite descartar Rascunho (pedidos já
    enviados para validação não podem ser apagados por aqui)."""
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    pedido = pedidos[pedidos["id"] == pedido_id]
    if pedido.empty:
        return False, "Pedido não encontrado."
    if pedido.iloc[0]["status"] != "Rascunho":
        return False, "Só é possível descartar pedidos em Rascunho."

    pedidos = pedidos[pedidos["id"] != pedido_id]
    pedidos.to_csv(_PEDIDOS_CSV, index=False)

    itens = pd.read_csv(_ITENS_CSV)
    itens = itens[itens["pedido_id"] != pedido_id]
    itens.to_csv(_ITENS_CSV, index=False)
    return True, "Pedido descartado."


def _recalcular_valor_total(pedido_id: int) -> None:
    """Recalcula pedidos.valor_total como soma dos subtotais (RN-004) dos itens do pedido."""
    df_itens = carregar_itens_pedido(pedido_id)
    total = float(df_itens["subtotal"].fillna(0).sum())

    pedidos = pd.read_csv(_PEDIDOS_CSV)
    mascara = pedidos["id"] == pedido_id
    pedidos.loc[mascara, "valor_total"] = total
    pedidos.loc[mascara, "updated_at"] = datetime.now().isoformat(timespec="seconds")
    pedidos.to_csv(_PEDIDOS_CSV, index=False)


def enviar_para_validacao(pedido_id: int) -> tuple[bool, str]:
    """Transiciona Rascunho -> Pendente Aprovação, se completo (RN-003)."""
    ok, mensagem = validar_pedido_completo(pedido_id)
    if not ok:
        return False, mensagem

    pedidos = pd.read_csv(_PEDIDOS_CSV)
    mascara = pedidos["id"] == pedido_id
    pedidos.loc[mascara, "status"] = "Pendente Aprovação"
    pedidos.loc[mascara, "updated_at"] = datetime.now().isoformat(timespec="seconds")
    pedidos.to_csv(_PEDIDOS_CSV, index=False)
    return True, "Pedido enviado para validação do trader."
