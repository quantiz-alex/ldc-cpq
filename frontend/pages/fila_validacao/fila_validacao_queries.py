"""Consultas e regras de dados da Fila de Validação do Trader.

RN-007: somente trader/admin podem aprovar, rejeitar ou devolver.
RN-008: rejeição e devolução exigem comentário.
RN-009: RTV não pode aprovar seus próprios pedidos.
RN-010: pedido devolvido volta para Rascunho.
RN-011: alertas de consistência não bloqueiam, mas exigem decisão explícita do trader.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent.parent / "mock_data"

_PEDIDOS_CSV = DATA_DIR / "pedidos.csv"
_CLIENTES_CSV = DATA_DIR / "clientes.csv"
_USUARIOS_CSV = DATA_DIR / "usuarios.csv"
_ALERTAS_CSV = DATA_DIR / "alertas_consistencia.csv"


def _carregar_base() -> pd.DataFrame:
    """Carrega pedidos com join de cliente, RTV e flag de alerta de consistência (RN-011)."""
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    clientes = pd.read_csv(_CLIENTES_CSV)
    usuarios = pd.read_csv(_USUARIOS_CSV)
    alertas = pd.read_csv(_ALERTAS_CSV)

    df = pedidos.merge(
        clientes[["id", "nome"]].rename(columns={"id": "cliente_id", "nome": "cliente_nome"}),
        on="cliente_id",
        how="left",
    )
    df = df.merge(
        usuarios[["id", "nome"]].rename(columns={"id": "rtv_id", "nome": "rtv_nome"}),
        on="rtv_id",
        how="left",
    )
    pedidos_com_alerta = set(alertas["pedido_id"].unique())
    df["com_alerta"] = df["id"].isin(pedidos_com_alerta).map({True: "Sim", False: "Não"})
    df["created_at"] = pd.to_datetime(df["created_at"])
    return df


def carregar_fila(
    status: str | None = None,
    rtv: str | None = None,
    com_alerta: str | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    apenas_pendentes: bool = False,
) -> pd.DataFrame:
    """Retorna a fila de pedidos filtrada (padrão: Pendente Aprovação quando apenas_pendentes)."""
    df = _carregar_base()

    if apenas_pendentes and not status:
        df = df[df["status"] == "Pendente Aprovação"]
    if status:
        df = df[df["status"] == status]
    if rtv:
        df = df[df["rtv_nome"] == rtv]
    if com_alerta:
        df = df[df["com_alerta"] == com_alerta]
    if data_inicio:
        df = df[df["created_at"] >= pd.to_datetime(data_inicio)]
    if data_fim:
        df = df[df["created_at"] <= pd.to_datetime(data_fim)]

    colunas = [
        "id",
        "cliente_nome",
        "rtv_id",
        "rtv_nome",
        "canal_origem",
        "valor_total",
        "status",
        "com_alerta",
        "aprovado_por",
        "aprovado_em",
        "comentario_aprovacao",
    ]
    return df[colunas].rename(columns={"cliente_nome": "cliente", "rtv_nome": "rtv"})


def calcular_kpis_fila() -> dict[str, float]:
    """Pendentes, aprovados hoje, rejeitados/devolvidos hoje e tempo médio de validação."""
    df = _carregar_base()
    hoje = pd.Timestamp.now().normalize()

    pendentes = int((df["status"] == "Pendente Aprovação").sum())

    df["aprovado_em_dt"] = pd.to_datetime(df["aprovado_em"], errors="coerce")
    hoje_mask = df["aprovado_em_dt"].dt.normalize() == hoje

    aprovados_hoje = int(((df["status"] == "Aprovado") & hoje_mask).sum())
    rejeitados_devolvidos_hoje = int(
        (df["status"].isin(["Rejeitado", "Devolvido"]) & hoje_mask).sum()
    )

    avaliados = df.dropna(subset=["aprovado_em_dt"])
    if not avaliados.empty:
        tempo_medio = float((avaliados["aprovado_em_dt"] - avaliados["created_at"]).dt.days.mean())
    else:
        tempo_medio = 0.0

    return {
        "pendentes": pendentes,
        "aprovados_hoje": aprovados_hoje,
        "rejeitados_devolvidos_hoje": rejeitados_devolvidos_hoje,
        "tempo_medio_dias": tempo_medio,
    }


def opcoes_rtv() -> list[dict]:
    """Opções de RTV para o filtro dropdown."""
    usuarios = pd.read_csv(_USUARIOS_CSV)
    rtvs = usuarios[usuarios["role"] == "rtv"]["nome"].dropna().unique()
    return [{"label": nome, "value": nome} for nome in sorted(rtvs)]


def obter_rtv_id(pedido_id: int) -> int | None:
    """RN-009 — retorna o rtv_id (autor) de um pedido, para bloquear auto-aprovação."""
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    linha = pedidos[pedidos["id"] == pedido_id]
    if linha.empty:
        return None
    return int(linha.iloc[0]["rtv_id"])


def atualizar_status_aprovacao(
    ids: list[int],
    novo_status: str,
    aprovado_por: str | None = None,
    comentario: str | None = None,
) -> int:
    """
    Atualiza o status dos pedidos (RN-007/008/010/011). 'Devolvido' retorna o
    pedido ao fluxo de edição do RTV (status intermediário — RN-010 diz que o
    pedido devolvido volta a Rascunho para reenvio).
    """
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    mascara = pedidos["id"].isin(ids)
    agora = datetime.now().isoformat(timespec="seconds")

    pedidos.loc[mascara, "status"] = novo_status
    pedidos.loc[mascara, "aprovado_por"] = aprovado_por or "sistema"
    pedidos.loc[mascara, "aprovado_em"] = agora
    if comentario:
        pedidos.loc[mascara, "comentario_aprovacao"] = comentario
    pedidos.loc[mascara, "updated_at"] = agora

    if novo_status == "Devolvido":
        # RN-010 — pedido devolvido volta ao status Rascunho para edição/reenvio do RTV
        pedidos.loc[mascara, "status"] = "Rascunho"

    pedidos.to_csv(_PEDIDOS_CSV, index=False)
    return int(mascara.sum())
