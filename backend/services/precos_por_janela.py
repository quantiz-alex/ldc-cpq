from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.precos_por_janela import PrecoPorJanela
from backend.repositories import precos_por_janela as repository
from backend.schemas.precos_por_janela import (
    PrecoLookupResponse,
    PrecoPorJanelaCreate,
    PrecoPorJanelaUpdate,
)

MENSAGEM_PRECO_NAO_ENCONTRADO = "Nenhum preço vigente encontrado para a combinação produto+janela+condição"


def listar(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    produto_id: int | None = None,
    janela_mes: int | None = None,
    janela_ano: int | None = None,
    condicao_pagamento: str | None = None,
) -> list[PrecoPorJanela]:
    return repository.get_all(
        db,
        skip=skip,
        limit=limit,
        produto_id=produto_id,
        janela_mes=janela_mes,
        janela_ano=janela_ano,
        condicao_pagamento=condicao_pagamento,
    )


def obter(db: Session, id: int) -> PrecoPorJanela:
    preco = repository.get_by_id(db, id)
    if preco is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return preco


def buscar_preco_vigente(
    db: Session,
    produto_id: int,
    janela_mes: int,
    janela_ano: int,
    condicao_pagamento: str,
    data_referencia: date | None = None,
) -> PrecoPorJanela | None:
    """RN-004: função reutilizável de lookup — chamada tanto pela rota GET /lookup
    quanto por backend/services/pedido_itens.py ao calcular preco_unitario/subtotal.
    """
    return repository.get_preco_vigente(
        db,
        produto_id=produto_id,
        janela_mes=janela_mes,
        janela_ano=janela_ano,
        condicao_pagamento=condicao_pagamento,
        data_referencia=data_referencia,
    )


def lookup(
    db: Session,
    produto_id: int,
    janela_mes: int,
    janela_ano: int,
    condicao_pagamento: str,
) -> PrecoLookupResponse:
    preco = buscar_preco_vigente(db, produto_id, janela_mes, janela_ano, condicao_pagamento)
    if preco is None:
        raise HTTPException(status_code=404, detail=MENSAGEM_PRECO_NAO_ENCONTRADO)
    return PrecoLookupResponse(
        preco_unitario=float(preco.preco),
        vigente_de=preco.vigente_de,
        vigente_ate=preco.vigente_ate,
    )


def criar(db: Session, data: PrecoPorJanelaCreate) -> PrecoPorJanela:
    return repository.create(db, data)


def atualizar(db: Session, id: int, data: PrecoPorJanelaUpdate) -> PrecoPorJanela:
    preco = repository.update(db, id, data)
    if preco is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return preco


def deletar(db: Session, id: int) -> None:
    if not repository.delete(db, id):
        raise HTTPException(status_code=404, detail="Registro não encontrado")
