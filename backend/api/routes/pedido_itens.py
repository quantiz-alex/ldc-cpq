from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.usuarios import Usuario
from backend.schemas.pedido_itens import PedidoItemCreate, PedidoItemResponse, PedidoItemUpdate
from backend.services import pedido_itens as service

router = APIRouter(prefix="/pedido-itens", tags=["PedidoItens"])


@router.get("/", response_model=list[PedidoItemResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    pedido_id: int | None = None,
    produto_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[PedidoItemResponse]:
    return service.listar(db, skip=skip, limit=limit, pedido_id=pedido_id, produto_id=produto_id)


@router.get("/{id}", response_model=PedidoItemResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoItemResponse:
    return service.obter(db, id)


@router.post("/", response_model=PedidoItemResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: PedidoItemCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoItemResponse:
    """Cria item de pedido. preco_unitario e subtotal são calculados via lookup em
    precos-por-janela (RN-004) — não editáveis manualmente. Valida soma parcelada (RN-006)."""
    return service.criar(db, data)


@router.put("/{id}", response_model=PedidoItemResponse)
def update(
    id: int,
    data: PedidoItemUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoItemResponse:
    return service.atualizar(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    service.deletar(db, id)
