from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.usuarios import Usuario
from backend.schemas.alertas_consistencia import (
    AlertaConsistenciaCreate,
    AlertaConsistenciaResponse,
    AlertaConsistenciaUpdate,
)
from backend.services import alertas_consistencia as service

router = APIRouter(prefix="/alertas-consistencia", tags=["AlertasConsistencia"])


@router.get("/", response_model=list[AlertaConsistenciaResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    pedido_id: int | None = None,
    severidade: str | None = None,
    tipo: str | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[AlertaConsistenciaResponse]:
    return service.listar(db, skip=skip, limit=limit, pedido_id=pedido_id, severidade=severidade, tipo=tipo)


@router.get("/{id}", response_model=AlertaConsistenciaResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> AlertaConsistenciaResponse:
    return service.obter(db, id)


@router.post("/", response_model=AlertaConsistenciaResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: AlertaConsistenciaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> AlertaConsistenciaResponse:
    """Gerado automaticamente pela análise de consistência — normalmente não criado manualmente."""
    return service.criar(db, data)


@router.put("/{id}", response_model=AlertaConsistenciaResponse)
def update(
    id: int,
    data: AlertaConsistenciaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> AlertaConsistenciaResponse:
    """Usado pelo trader para registrar resolvido_por ao decidir sobre um pedido com alerta (RN-011)."""
    return service.atualizar(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    service.deletar(db, id)
