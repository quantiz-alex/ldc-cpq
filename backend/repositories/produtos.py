from sqlalchemy.orm import Session

from backend.models.produtos import Produto
from backend.schemas.produtos import ProdutoCreate, ProdutoUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Produto]:
    return (
        db.query(Produto)
        .filter(Produto.ativo == True)  # noqa: E712
        .order_by(Produto.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_by_id(db: Session, id: int) -> Produto | None:
    return db.query(Produto).filter(Produto.id == id).first()


def create(db: Session, data: ProdutoCreate) -> Produto:
    produto = Produto(**data.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def update(db: Session, id: int, data: ProdutoUpdate) -> Produto | None:
    produto = get_by_id(db, id)
    if produto is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(produto, field, value)
    db.commit()
    db.refresh(produto)
    return produto


def delete(db: Session, id: int) -> bool:
    produto = get_by_id(db, id)
    if produto is None:
        return False
    produto.ativo = False
    db.commit()
    return True
