"""Consultas de dados de Relatórios Comerciais.

RN-015: relatórios respeitam o escopo de carteira/região do usuário — regra
marcada needs_review (parsed:false) em docs/business_logic.yaml. A condição de
RBAC já descrita (RTV -> própria carteira; trader/admin -> sem restrição) é
implementada abaixo, mas recomenda-se validação de negócio adicional.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent.parent / "mock_data"

_PEDIDOS_CSV = DATA_DIR / "pedidos.csv"
_CLIENTES_CSV = DATA_DIR / "clientes.csv"
_USUARIOS_CSV = DATA_DIR / "usuarios.csv"


def carregar_relatorio(
    data_inicio: str | None = None,
    data_fim: str | None = None,
    rtv: str | None = None,
    regiao: str | None = None,
    cliente: str | None = None,
    linha_produto: str | None = None,
    user_role: str | None = None,
    user_id: int | None = None,
) -> pd.DataFrame:
    """Retorna pedidos filtrados para o relatório (RN-015: escopo por carteira/região)."""
    pedidos = pd.read_csv(_PEDIDOS_CSV)
    clientes = pd.read_csv(_CLIENTES_CSV)
    usuarios = pd.read_csv(_USUARIOS_CSV)

    df = pedidos.merge(
        clientes[["id", "nome", "regiao"]].rename(columns={"id": "cliente_id", "nome": "cliente_nome"}),
        on="cliente_id",
        how="left",
    )
    df = df.merge(
        usuarios[["id", "nome"]].rename(columns={"id": "rtv_id", "nome": "rtv_nome"}),
        on="rtv_id",
        how="left",
    )
    df["created_at"] = pd.to_datetime(df["created_at"])

    if user_role == "rtv" and user_id is not None:
        df = df[df["rtv_id"] == user_id]

    if data_inicio:
        df = df[df["created_at"] >= pd.to_datetime(data_inicio)]
    if data_fim:
        df = df[df["created_at"] <= pd.to_datetime(data_fim)]
    if rtv:
        df = df[df["rtv_nome"] == rtv]
    if regiao:
        df = df[df["regiao"] == regiao]
    if cliente:
        df = df[df["cliente_nome"] == cliente]

    if linha_produto:
        itens = pd.read_csv(DATA_DIR / "pedido_itens.csv")
        produtos = pd.read_csv(DATA_DIR / "produtos.csv")
        itens = itens.merge(
            produtos[["id", "tipo"]].rename(columns={"id": "produto_id"}), on="produto_id", how="left"
        )
        pedido_ids = itens.loc[itens["tipo"] == linha_produto, "pedido_id"].unique()
        df = df[df["id"].isin(pedido_ids)]

    colunas = ["id", "cliente_nome", "rtv_nome", "valor_total", "status", "created_at"]
    return df[colunas].rename(columns={"cliente_nome": "cliente", "rtv_nome": "rtv"})


def dados_grafico_receita_periodo(df: pd.DataFrame) -> tuple[list, dict[str, list]]:
    """Série mensal de receita por RTV (top 5)."""
    if df.empty:
        return [], {}
    df = df.copy()
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["mes"] = df["created_at"].dt.strftime("%Y-%m")
    top_rtvs = df.groupby("rtv")["valor_total"].sum().sort_values(ascending=False).head(5).index

    pivot = (
        df[df["rtv"].isin(top_rtvs)]
        .pivot_table(index="mes", columns="rtv", values="valor_total", aggfunc="sum", fill_value=0)
        .sort_index()
    )
    x = list(pivot.index)
    series = {col: pivot[col].tolist() for col in pivot.columns}
    return x, series


def dados_grafico_eficiencia(df: pd.DataFrame) -> tuple[list, list]:
    """Contagem de pedidos por status — proxy de eficiência de triagem."""
    if df.empty:
        return [], []
    contagem = df["status"].value_counts()
    return list(contagem.index), [int(v) for v in contagem.values]


def opcoes_rtv() -> list[dict]:
    """Opções de RTV para o filtro dropdown."""
    usuarios = pd.read_csv(_USUARIOS_CSV)
    rtvs = usuarios[usuarios["role"] == "rtv"]["nome"].dropna().unique()
    return [{"label": nome, "value": nome} for nome in sorted(rtvs)]


def opcoes_regiao() -> list[dict]:
    """Opções de região para o filtro dropdown."""
    clientes = pd.read_csv(_CLIENTES_CSV)
    return [{"label": r, "value": r} for r in sorted(clientes["regiao"].dropna().unique())]


def opcoes_cliente() -> list[dict]:
    """Opções de cliente para o filtro dropdown."""
    clientes = pd.read_csv(_CLIENTES_CSV)
    return [{"label": n, "value": n} for n in sorted(clientes["nome"].dropna().unique())]


def opcoes_linha_produto() -> list[dict]:
    """Opções de linha de produto para o filtro dropdown."""
    return [
        {"label": "Defensivos", "value": "Defensivo"},
        {"label": "Fertilizantes", "value": "Fertilizante"},
    ]
