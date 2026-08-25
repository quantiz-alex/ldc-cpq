from sqlalchemy.orm import Session

from backend.models.pedido_itens import PedidoItem


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    pedido_id: int | None = None,
    produto_id: int | None = None,
) -> list[PedidoItem]:
    query = db.query(PedidoItem)
    if pedido_id is not None:
        query = query.filter(PedidoItem.pedido_id == pedido_id)
    if produto_id is not None:
        query = query.filter(PedidoItem.produto_id == produto_id)
    return query.order_by(PedidoItem.id).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int) -> PedidoItem | None:
    return db.query(PedidoItem).filter(PedidoItem.id == id).first()


def create(db: Session, payload: dict) -> PedidoItem:
    item = PedidoItem(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update(db: Session, id: int, payload: dict) -> PedidoItem | None:
    item = get_by_id(db, id)
    if item is None:
        return None
    for field, value in payload.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, id: int) -> bool:
    item = get_by_id(db, id)
    if item is None:
        return False
    db.delete(item)
    db.commit()
    return True
