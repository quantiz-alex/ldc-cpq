"""Consultas de dados do Dashboard Comercial — leitura via mock_data/*.csv (pandas).

RN-001: RTV só vê a própria carteira; trader/admin veem toda a região sob responsabilidade.
RN-002: KPIs de receita só somam pedidos com status == 'Aprovado'.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent.parent / "mock_data"


def _carregar_base() -> pd.DataFrame:
    """Carrega pedidos com join de cliente (região) e RTV (usuários)."""
    pedidos = pd.read_csv(DATA_DIR / "pedidos.csv")
    clientes = pd.read_csv(DATA_DIR / "clientes.csv")
    usuarios = pd.read_csv(DATA_DIR / "usuarios.csv")

    df = pedidos.merge(
        clientes[["id", "nome", "regiao"]].rename(
            columns={"id": "cliente_id", "nome": "cliente_nome"}
        ),
        on="cliente_id",
        how="left",
    )
    df = df.merge(
        usuarios[["id", "nome"]].rename(columns={"id": "rtv_id", "nome": "rtv_nome"}),
        on="rtv_id",
        how="left",
    )
    df["created_at"] = pd.to_datetime(df["created_at"])
    return df


def _filtrar_linha_produto(df: pd.DataFrame, linha_produto: str | None) -> pd.DataFrame:
    """Filtra pedidos que possuem ao menos um item da linha (Defensivo/Fertilizante)."""
    if not linha_produto or df.empty:
        return df
    itens = pd.read_csv(DATA_DIR / "pedido_itens.csv")
    produtos = pd.read_csv(DATA_DIR / "produtos.csv")
    itens = itens.merge(
        produtos[["id", "tipo"]].rename(columns={"id": "produto_id"}),
        on="produto_id",
        how="left",
    )
    pedido_ids = itens.loc[itens["tipo"] == linha_produto, "pedido_id"].unique()
    return df[df["id"].isin(pedido_ids)]


def carregar_pedidos(
    data_inicio: str | None = None,
    data_fim: str | None = None,
    rtv: str | None = None,
    regiao: str | None = None,
    linha_produto: str | None = None,
    status: str | None = None,
    user_role: str | None = None,
    user_id: int | None = None,
) -> pd.DataFrame:
    """Retorna pedidos filtrados respeitando o escopo do usuário (RN-001)."""
    df = _carregar_base()

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
    if status:
        df = df[df["status"] == status]

    df = _filtrar_linha_produto(df, linha_produto)
    return df.copy()


def calcular_kpis(df: pd.DataFrame) -> dict[str, float]:
    """Calcula os 6 KPIs do dashboard (RN-002: receita só de pedidos Aprovado)."""
    aprovados = df[df["status"] == "Aprovado"]
    pendentes = df[df["status"] == "Pendente Aprovação"]

    total_pedidos = int(len(df))
    receita = float(aprovados["valor_total"].sum())
    ticket_medio = float(aprovados["valor_total"].mean()) if len(aprovados) else 0.0
    qtd_pendentes = int(len(pendentes))

    if len(pendentes):
        tempo_medio_dias = float((pd.Timestamp.now() - pendentes["created_at"]).dt.days.mean())
    else:
        tempo_medio_dias = 0.0

    alertas = pd.read_csv(DATA_DIR / "alertas_consistencia.csv")
    pedidos_com_alerta = int(df[df["id"].isin(alertas["pedido_id"])].shape[0])
    pct_com_alerta = (pedidos_com_alerta / total_pedidos * 100) if total_pedidos else 0.0

    return {
        "pedidos_captados": total_pedidos,
        "receita_acumulada": receita,
        "ticket_medio": ticket_medio,
        "pendentes_validacao": qtd_pendentes,
        "tempo_medio_triagem": tempo_medio_dias,
        "pct_com_alerta": pct_com_alerta,
    }


def dados_grafico_receita_semana(df: pd.DataFrame) -> tuple[list, dict[str, list]]:
    """Série semanal de receita quebrada por linha de produto (Defensivo x Fertilizante)."""
    vazio: dict[str, list] = {"Defensivos": [], "Fertilizantes": []}
    if df.empty:
        return [], vazio

    itens = pd.read_csv(DATA_DIR / "pedido_itens.csv")
    produtos = pd.read_csv(DATA_DIR / "produtos.csv")
    # Descarta o "created_at" próprio de pedido_itens (irrelevante aqui) para evitar
    # colisão de nome com o "created_at" de pedidos após o merge abaixo.
    itens = itens.drop(columns=["created_at"], errors="ignore").merge(
        produtos[["id", "tipo"]].rename(columns={"id": "produto_id"}),
        on="produto_id",
        how="left",
    )
    itens = itens.merge(
        df[["id", "created_at"]].rename(columns={"id": "pedido_id"}),
        on="pedido_id",
        how="inner",
    )
    if itens.empty:
        return [], vazio

    itens["semana"] = itens["created_at"].dt.to_period("W").apply(
        lambda p: p.start_time.strftime("%d/%m")
    )
    pivot = itens.pivot_table(
        index="semana", columns="tipo", values="subtotal", aggfunc="sum", fill_value=0
    ).sort_index()

    x = list(pivot.index)
    series = {
        "Defensivos": pivot["Defensivo"].tolist() if "Defensivo" in pivot else [0] * len(x),
        "Fertilizantes": pivot["Fertilizante"].tolist() if "Fertilizante" in pivot else [0] * len(x),
    }
    return x, series


def dados_grafico_top_rtv(df: pd.DataFrame, top_n: int = 8) -> tuple[list, list]:
    """Top RTVs por receita captada (apenas pedidos Aprovado — RN-002)."""
    aprovados = df[df["status"] == "Aprovado"]
    if aprovados.empty:
        return [], []
    ranking = (
        aprovados.groupby("rtv_nome")["valor_total"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )
    return list(ranking.index), [float(v) for v in ranking.values]


def opcoes_rtv() -> list[dict]:
    """Opções para o filtro dropdown de RTV."""
    usuarios = pd.read_csv(DATA_DIR / "usuarios.csv")
    rtvs = usuarios[usuarios["role"] == "rtv"]["nome"].dropna().unique()
    return [{"label": nome, "value": nome} for nome in sorted(rtvs)]


def opcoes_regiao() -> list[dict]:
    """Opções para o filtro dropdown de região."""
    clientes = pd.read_csv(DATA_DIR / "clientes.csv")
    regioes = clientes["regiao"].dropna().unique()
    return [{"label": r, "value": r} for r in sorted(regioes)]
