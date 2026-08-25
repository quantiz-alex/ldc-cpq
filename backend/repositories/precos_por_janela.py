from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.models.precos_por_janela import PrecoPorJanela
from backend.schemas.precos_por_janela import PrecoPorJanelaCreate, PrecoPorJanelaUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    produto_id: int | None = None,
    janela_mes: int | None = None,
    janela_ano: int | None = None,
    condicao_pagamento: str | None = None,
) -> list[PrecoPorJanela]:
    query = db.query(PrecoPorJanela)
    if produto_id is not None:
        query = query.filter(PrecoPorJanela.produto_id == produto_id)
    if janela_mes is not None:
        query = query.filter(PrecoPorJanela.janela_mes == janela_mes)
    if janela_ano is not None:
        query = query.filter(PrecoPorJanela.janela_ano == janela_ano)
    if condicao_pagamento is not None:
        query = query.filter(PrecoPorJanela.condicao_pagamento == condicao_pagamento)
    return query.order_by(PrecoPorJanela.id).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int) -> PrecoPorJanela | None:
    return db.query(PrecoPorJanela).filter(PrecoPorJanela.id == id).first()


def get_preco_vigente(
    db: Session,
    produto_id: int,
    janela_mes: int,
    janela_ano: int,
    condicao_pagamento: str,
    data_referencia: date | None = None,
) -> PrecoPorJanela | None:
    """RN-004: lookup do preço vigente por produto + janela de entrega + condição comercial."""
    referencia = data_referencia or date.today()
    return (
        db.query(PrecoPorJanela)
        .filter(
            PrecoPorJanela.produto_id == produto_id,
            PrecoPorJanela.janela_mes == janela_mes,
            PrecoPorJanela.janela_ano == janela_ano,
            PrecoPorJanela.condicao_pagamento == condicao_pagamento,
            PrecoPorJanela.vigente_de <= referencia,
            or_(PrecoPorJanela.vigente_ate.is_(None), PrecoPorJanela.vigente_ate >= referencia),
        )
        .order_by(PrecoPorJanela.vigente_de.desc())
        .first()
    )


def create(db: Session, data: PrecoPorJanelaCreate) -> PrecoPorJanela:
    preco = PrecoPorJanela(**data.model_dump())
    db.add(preco)
    db.commit()
    db.refresh(preco)
    return preco


def update(db: Session, id: int, data: PrecoPorJanelaUpdate) -> PrecoPorJanela | None:
    preco = get_by_id(db, id)
    if preco is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(preco, field, value)
    db.commit()
    db.refresh(preco)
    return preco


def delete(db: Session, id: int) -> bool:
    preco = get_by_id(db, id)
    if preco is None:
        return False
    db.delete(preco)
    db.commit()
    return True
