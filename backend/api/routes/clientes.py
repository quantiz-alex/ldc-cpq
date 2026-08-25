from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.usuarios import Usuario
from backend.schemas.clientes import ClienteCreate, ClienteResponse, ClienteUpdate
from backend.services import clientes as service

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=list[ClienteResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    regiao: str | None = None,
    rtv_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[ClienteResponse]:
    """Escopo: RTV só vê própria carteira (RN-001)."""
    return service.listar(db, current_user, skip=skip, limit=limit, regiao=regiao, rtv_id=rtv_id)


@router.get("/{id}", response_model=ClienteResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ClienteResponse:
    return service.obter(db, id)


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ClienteResponse:
    return service.criar(db, data)


@router.put("/{id}", response_model=ClienteResponse)
def update(
    id: int,
    data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ClienteResponse:
    return service.atualizar(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    """Soft delete — marca ativo=false."""
    service.deletar(db, id)
