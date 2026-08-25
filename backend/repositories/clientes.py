from sqlalchemy.orm import Session

from backend.models.clientes import Cliente
from backend.schemas.clientes import ClienteCreate, ClienteUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    regiao: str | None = None,
    rtv_id: int | None = None,
) -> list[Cliente]:
    query = db.query(Cliente).filter(Cliente.ativo == True)  # noqa: E712
    if regiao is not None:
        query = query.filter(Cliente.regiao == regiao)
    if rtv_id is not None:
        query = query.filter(Cliente.rtv_id == rtv_id)
    return query.order_by(Cliente.id).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int) -> Cliente | None:
    return db.query(Cliente).filter(Cliente.id == id).first()


def create(db: Session, data: ClienteCreate) -> Cliente:
    cliente = Cliente(**data.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def update(db: Session, id: int, data: ClienteUpdate) -> Cliente | None:
    cliente = get_by_id(db, id)
    if cliente is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cliente, field, value)
    db.commit()
    db.refresh(cliente)
    return cliente


def delete(db: Session, id: int) -> bool:
    cliente = get_by_id(db, id)
    if cliente is None:
        return False
    cliente.ativo = False
    db.commit()
    return True
