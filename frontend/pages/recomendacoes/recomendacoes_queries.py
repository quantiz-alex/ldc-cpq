"""Consultas de dados do Motor de Recomendação (Cross-sell).

ATENÇÃO — RN-013 (score) está marcada parsed: false / needs_review em
docs/business_logic.yaml: o roadmap não especifica os pesos de recência,
frequência, volume histórico e sazonalidade. Por isso o campo `score` é lido
diretamente de mock_data/recomendacoes.csv (já populado pelo data-engineer),
SEM inventar fórmula/pesos no frontend. Ver aviso no relatório final do
frontend-builder — recomenda-se detalhar RN-013 no roadmap antes de
implementar o cálculo real do score em um serviço de backend.

RN-012: recomendações nunca criam pedido automaticamente — apenas navegação
para a Captação de Pedido, onde o RTV adiciona manualmente o item.
RN-014: RTV só vê recomendações dos clientes de sua carteira.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent.parent / "mock_data"

_RECOMENDACOES_CSV = DATA_DIR / "recomendacoes.csv"
_CLIENTES_CSV = DATA_DIR / "clientes.csv"
_PRODUTOS_CSV = DATA_DIR / "produtos.csv"


def carregar_recomendacoes(
    cliente: str | None = None,
    cultura_safra: str | None = None,
    regiao: str | None = None,
    linha_produto: str | None = None,
    user_role: str | None = None,
    user_id: int | None = None,
) -> pd.DataFrame:
    """Retorna recomendações filtradas. RN-014: RTV só vê clientes de sua carteira."""
    recomendacoes = pd.read_csv(_RECOMENDACOES_CSV)
    clientes = pd.read_csv(_CLIENTES_CSV)
    produtos = pd.read_csv(_PRODUTOS_CSV)

    if user_role == "rtv" and user_id is not None:
        carteira_ids = clientes.loc[clientes["rtv_id"] == user_id, "id"]
        recomendacoes = recomendacoes[recomendacoes["cliente_id"].isin(carteira_ids)]

    df = recomendacoes.merge(
        clientes[["id", "nome", "regiao", "cultura_principal"]].rename(
            columns={"id": "cliente_id", "nome": "cliente_nome"}
        ),
        on="cliente_id",
        how="left",
    )
    df = df.merge(
        produtos[["id", "nome_comercial", "tipo"]].rename(columns={"id": "produto_id"}),
        on="produto_id",
        how="left",
    )

    if cliente:
        df = df[df["cliente_nome"] == cliente]
    if cultura_safra:
        df = df[df["cultura_principal"] == cultura_safra]
    if regiao:
        df = df[df["regiao"] == regiao]
    if linha_produto:
        df = df[df["tipo"] == linha_produto]

    df["aceita"] = df["aceita"].map({1: "Sim", 0: "Não", True: "Sim", False: "Não"})

    colunas = [
        "id",
        "cliente_id",
        "cliente_nome",
        "produto_id",
        "nome_comercial",
        "motivo",
        "score",
        "aceita",
        "gerada_em",
    ]
    return df[colunas].rename(
        columns={"cliente_nome": "cliente", "nome_comercial": "produto"}
    )


def calcular_kpis(df: pd.DataFrame) -> dict[str, float]:
    """% aceitos, receita incremental estimada e cobertura da carteira."""
    total = int(len(df))
    aceitos = int((df["aceita"] == "Sim").sum())
    pct_aceitos = (aceitos / total * 100) if total else 0.0

    produtos = pd.read_csv(_PRODUTOS_CSV)
    df_com_custo = df.merge(
        produtos[["id", "custo"]].rename(columns={"id": "produto_id"}), on="produto_id", how="left"
    )
    receita_incremental = float(
        df_com_custo.loc[df_com_custo["aceita"] == "Sim", "custo"].fillna(0).sum()
    )

    clientes = pd.read_csv(_CLIENTES_CSV)
    total_clientes = int(clientes["ativo"].sum())
    clientes_com_recomendacao = int(df["cliente_id"].nunique())
    cobertura = (clientes_com_recomendacao / total_clientes * 100) if total_clientes else 0.0

    return {
        "pct_aceitos": pct_aceitos,
        "receita_incremental": receita_incremental,
        "cobertura_carteira": cobertura,
    }


def dados_grafico_top_produtos(df: pd.DataFrame, top_n: int = 8) -> tuple[list, list]:
    """Ranking de produtos mais recomendados no período (contagem de sugestões)."""
    if df.empty:
        return [], []
    ranking = df.groupby("produto")["id"].count().sort_values(ascending=False).head(top_n)
    return list(ranking.index), [int(v) for v in ranking.values]


def opcoes_clientes() -> list[dict]:
    """Opções de cliente para o filtro dropdown."""
    clientes = pd.read_csv(_CLIENTES_CSV)
    return [{"label": nome, "value": nome} for nome in sorted(clientes["nome"].dropna().unique())]


def opcoes_cultura_safra() -> list[dict]:
    """Opções de cultura principal para o filtro dropdown."""
    clientes = pd.read_csv(_CLIENTES_CSV)
    culturas = clientes["cultura_principal"].dropna().unique()
    return [{"label": c, "value": c} for c in sorted(culturas)]


def opcoes_regiao() -> list[dict]:
    """Opções de região para o filtro dropdown."""
    clientes = pd.read_csv(_CLIENTES_CSV)
    return [{"label": r, "value": r} for r in sorted(clientes["regiao"].dropna().unique())]


def opcoes_linha_produto() -> list[dict]:
    """Opções de linha de produto para o filtro dropdown."""
    return [
        {"label": "Defensivos", "value": "Defensivo"},
        {"label": "Fertilizantes", "value": "Fertilizante"},
    ]
