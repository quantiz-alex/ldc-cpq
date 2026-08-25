from sqlalchemy.orm import Session

from backend.models.recomendacoes import Recomendacao
from backend.schemas.recomendacoes import RecomendacaoCreate, RecomendacaoUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    cliente_id: int | None = None,
    produto_id: int | None = None,
    motivo: str | None = None,
    aceita: bool | None = None,
) -> list[Recomendacao]:
    query = db.query(Recomendacao)
    if cliente_id is not None:
        query = query.filter(Recomendacao.cliente_id == cliente_id)
    if produto_id is not None:
        query = query.filter(Recomendacao.produto_id == produto_id)
    if motivo is not None:
        query = query.filter(Recomendacao.motivo == motivo)
    if aceita is not None:
        query = query.filter(Recomendacao.aceita == aceita)
    return query.order_by(Recomendacao.id).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int) -> Recomendacao | None:
    return db.query(Recomendacao).filter(Recomendacao.id == id).first()


def create(db: Session, data: RecomendacaoCreate) -> Recomendacao:
    recomendacao = Recomendacao(**data.model_dump(), aceita=False)
    db.add(recomendacao)
    db.commit()
    db.refresh(recomendacao)
    return recomendacao


def update(db: Session, id: int, data: RecomendacaoUpdate) -> Recomendacao | None:
    recomendacao = get_by_id(db, id)
    if recomendacao is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(recomendacao, field, value)
    db.commit()
    db.refresh(recomendacao)
    return recomendacao


def delete(db: Session, id: int) -> bool:
    recomendacao = get_by_id(db, id)
    if recomendacao is None:
        return False
    db.delete(recomendacao)
    db.commit()
    return True
