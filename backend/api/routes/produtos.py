from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.usuarios import Usuario
from backend.schemas.produtos import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from backend.services import produtos as service

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/", response_model=list[ProdutoResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[ProdutoResponse]:
    return service.listar(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=ProdutoResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ProdutoResponse:
    return service.obter(db, id)


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ProdutoResponse:
    """Cria produto — somente admin (RN-016, manutenção de catálogo)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para esta operação")
    return service.criar(db, data)


@router.put("/{id}", response_model=ProdutoResponse)
def update(
    id: int,
    data: ProdutoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ProdutoResponse:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para esta operação")
    return service.atualizar(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    """Soft delete — marca ativo=false. Somente admin (RN-016)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para esta operação")
    service.deletar(db, id)
