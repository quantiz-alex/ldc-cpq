from sqlalchemy.orm import Session

from backend.models.alertas_consistencia import AlertaConsistencia
from backend.schemas.alertas_consistencia import AlertaConsistenciaCreate, AlertaConsistenciaUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    pedido_id: int | None = None,
    severidade: str | None = None,
    tipo: str | None = None,
) -> list[AlertaConsistencia]:
    query = db.query(AlertaConsistencia)
    if pedido_id is not None:
        query = query.filter(AlertaConsistencia.pedido_id == pedido_id)
    if severidade is not None:
        query = query.filter(AlertaConsistencia.severidade == severidade)
    if tipo is not None:
        query = query.filter(AlertaConsistencia.tipo == tipo)
    return query.order_by(AlertaConsistencia.id).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int) -> AlertaConsistencia | None:
    return db.query(AlertaConsistencia).filter(AlertaConsistencia.id == id).first()


def create(db: Session, data: AlertaConsistenciaCreate) -> AlertaConsistencia:
    alerta = AlertaConsistencia(**data.model_dump())
    db.add(alerta)
    db.commit()
    db.refresh(alerta)
    return alerta


def update(db: Session, id: int, data: AlertaConsistenciaUpdate) -> AlertaConsistencia | None:
    alerta = get_by_id(db, id)
    if alerta is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(alerta, field, value)
    db.commit()
    db.refresh(alerta)
    return alerta


def delete(db: Session, id: int) -> bool:
    alerta = get_by_id(db, id)
    if alerta is None:
        return False
    db.delete(alerta)
    db.commit()
    return True
