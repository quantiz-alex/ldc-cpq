from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.models.pedido_itens import PedidoItem
from backend.repositories import pedido_itens as repository
from backend.schemas.pedido_itens import PedidoItemCreate, PedidoItemUpdate
from backend.services import precos_por_janela as precos_service


def listar(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    pedido_id: int | None = None,
    produto_id: int | None = None,
) -> list[PedidoItem]:
    return repository.get_all(db, skip=skip, limit=limit, pedido_id=pedido_id, produto_id=produto_id)


def obter(db: Session, id: int) -> PedidoItem:
    item = repository.get_by_id(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return item


def calcular_precificacao(
    db: Session,
    produto_id: int,
    janela_mes: int,
    janela_ano: int,
    condicao_pagamento: str,
    quantidade: float,
) -> tuple[float, float]:
    """RN-004: precificação automática por lookup em precos_por_janela — chamada por
    criar() e atualizar() abaixo (ambas invocadas pelas rotas POST/PUT de
    backend/api/routes/pedido_itens.py). Nunca é uma fórmula ajustável por slider: o
    preço é sempre o resultado determinístico deste lookup, recalculado sempre que
    produto/janela/condição mudam no grid de itens.

    subtotal = quantidade * preco_unitario (mesma fórmula usada em formula.expression
    de docs/business_logic.yaml — RN-004).
    """
    preco_vigente = precos_service.buscar_preco_vigente(
        db,
        produto_id=produto_id,
        janela_mes=janela_mes,
        janela_ano=janela_ano,
        condicao_pagamento=condicao_pagamento,
    )
    if preco_vigente is None:
        raise HTTPException(
            status_code=422,
            detail="Nenhum preço vigente encontrado para a combinação produto+janela+condição",
        )
    preco_unitario = float(preco_vigente.preco)
    subtotal = round(quantidade * preco_unitario, 2)
    return preco_unitario, subtotal


def criar(db: Session, data: PedidoItemCreate) -> PedidoItem:
    """RN-006: revalida o schema com contexto de DB para aplicar a checagem real de soma
    parcelada (ver backend/schemas/pedido_itens.py::PedidoItemCreate.validar_soma_parcelada).
    RN-004: calcula preco_unitario/subtotal via lookup antes de persistir — edição manual do
    preço não é aceita neste endpoint (exige permissão específica de override, fora de escopo
    do CRUD padrão).
    """
    try:
        PedidoItemCreate.model_validate(data.model_dump(), context={"db": db})
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()[0]["msg"]) from exc

    preco_unitario, subtotal = calcular_precificacao(
        db,
        produto_id=data.produto_id,
        janela_mes=data.janela_mes,
        janela_ano=data.janela_ano,
        condicao_pagamento=data.condicao_pagamento,
        quantidade=data.quantidade,
    )

    payload = data.model_dump(exclude={"quantidade_total_esperada"})
    payload["preco_unitario"] = preco_unitario
    payload["subtotal"] = subtotal
    return repository.create(db, payload)


def atualizar(db: Session, id: int, data: PedidoItemUpdate) -> PedidoItem:
    item = repository.get_by_id(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    try:
        PedidoItemUpdate.model_validate(
            data.model_dump(exclude_unset=True),
            context={
                "db": db,
                "pedido_id": item.pedido_id,
                "produto_id": item.produto_id,
                "item_id": id,
            },
        )
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()[0]["msg"]) from exc

    campos_atualizados = data.model_dump(exclude_unset=True, exclude={"quantidade_total_esperada"})

    # RN-004: se algum campo-chave do lookup (ou a quantidade) mudou, recalcula preco_unitario/subtotal.
    campos_lookup = {"janela_mes", "janela_ano", "condicao_pagamento", "quantidade"}
    if campos_lookup.intersection(campos_atualizados.keys()):
        janela_mes = campos_atualizados.get("janela_mes", item.janela_mes)
        janela_ano = campos_atualizados.get("janela_ano", item.janela_ano)
        condicao_pagamento = campos_atualizados.get("condicao_pagamento", item.condicao_pagamento)
        quantidade = campos_atualizados.get("quantidade", float(item.quantidade))
        preco_unitario, subtotal = calcular_precificacao(
            db,
            produto_id=item.produto_id,
            janela_mes=janela_mes,
            janela_ano=janela_ano,
            condicao_pagamento=condicao_pagamento,
            quantidade=quantidade,
        )
        campos_atualizados["preco_unitario"] = preco_unitario
        campos_atualizados["subtotal"] = subtotal

    item_atualizado = repository.update(db, id, campos_atualizados)
    if item_atualizado is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return item_atualizado


def deletar(db: Session, id: int) -> None:
    if not repository.delete(db, id):
        raise HTTPException(status_code=404, detail="Registro não encontrado")
