from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.usuarios import Usuario
from backend.schemas.usuarios import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from backend.services import usuarios as service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[UsuarioResponse]:
    return service.listar(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=UsuarioResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> UsuarioResponse:
    return service.obter(db, id)


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> UsuarioResponse:
    """Cria usuário — somente admin (RN-016)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para esta operação")
    return service.criar(db, data)


@router.put("/{id}", response_model=UsuarioResponse)
def update(
    id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> UsuarioResponse:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para esta operação")
    return service.atualizar(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    """Soft delete (ativo=false) — somente admin (RN-016)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para esta operação")
    service.deletar(db, id)
