from datetime import date

from sqlalchemy.orm import Session

from backend.models.pedidos import Pedido
from backend.schemas.pedidos import PedidoCreate, PedidoUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    rtv_id: int | None = None,
    cliente_id: int | None = None,
    data_pedido_de: date | None = None,
    data_pedido_ate: date | None = None,
) -> list[Pedido]:
    query = db.query(Pedido)
    if status is not None:
        query = query.filter(Pedido.status == status)
    if rtv_id is not None:
        query = query.filter(Pedido.rtv_id == rtv_id)
    if cliente_id is not None:
        query = query.filter(Pedido.cliente_id == cliente_id)
    if data_pedido_de is not None:
        query = query.filter(Pedido.created_at >= data_pedido_de)
    if data_pedido_ate is not None:
        query = query.filter(Pedido.created_at <= data_pedido_ate)
    return query.order_by(Pedido.id).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int) -> Pedido | None:
    return db.query(Pedido).filter(Pedido.id == id).first()


def create(db: Session, data: PedidoCreate) -> Pedido:
    pedido = Pedido(**data.model_dump(), status="Rascunho", valor_total=0)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


def update(db: Session, id: int, data: PedidoUpdate) -> Pedido | None:
    pedido = get_by_id(db, id)
    if pedido is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pedido, field, value)
    db.commit()
    db.refresh(pedido)
    return pedido


def delete(db: Session, id: int) -> bool:
    pedido = get_by_id(db, id)
    if pedido is None:
        return False
    db.delete(pedido)
    db.commit()
    return True
