from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.alertas_consistencia import AlertaConsistencia
from backend.repositories import alertas_consistencia as repository
from backend.schemas.alertas_consistencia import AlertaConsistenciaCreate, AlertaConsistenciaUpdate


def listar(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    pedido_id: int | None = None,
    severidade: str | None = None,
    tipo: str | None = None,
) -> list[AlertaConsistencia]:
    return repository.get_all(
        db, skip=skip, limit=limit, pedido_id=pedido_id, severidade=severidade, tipo=tipo
    )


def obter(db: Session, id: int) -> AlertaConsistencia:
    alerta = repository.get_by_id(db, id)
    if alerta is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return alerta


def criar(db: Session, data: AlertaConsistenciaCreate) -> AlertaConsistencia:
    return repository.create(db, data)


def atualizar(db: Session, id: int, data: AlertaConsistenciaUpdate) -> AlertaConsistencia:
    """RN-011: usado pelo trader para registrar resolvido_por ao decidir sobre um pedido com
    alerta — o alerta não bloqueia a decisão, mas exige registro explícito."""
    alerta = repository.update(db, id, data)
    if alerta is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return alerta


def deletar(db: Session, id: int) -> None:
    if not repository.delete(db, id):
        raise HTTPException(status_code=404, detail="Registro não encontrado")
