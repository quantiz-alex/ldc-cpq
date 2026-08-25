from datetime import date

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.usuarios import Usuario
from backend.schemas.pedidos import (
    ApproveRequest,
    PedidoCreate,
    PedidoResponse,
    PedidoUpdate,
    RejectRequest,
    ReturnRequest,
)
from backend.services import pedidos as service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/", response_model=list[PedidoResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    status_filtro: str | None = None,
    rtv_id: int | None = None,
    cliente_id: int | None = None,
    data_pedido_de: date | None = None,
    data_pedido_ate: date | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[PedidoResponse]:
    """Escopo: RTV vê apenas própria carteira (RN-001)."""
    return service.listar(
        db,
        current_user,
        skip=skip,
        limit=limit,
        status=status_filtro,
        rtv_id=rtv_id,
        cliente_id=cliente_id,
        data_pedido_de=data_pedido_de,
        data_pedido_ate=data_pedido_ate,
    )


@router.get("/{id}", response_model=PedidoResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoResponse:
    return service.obter(db, id)


@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: PedidoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoResponse:
    """Cria pedido em status Rascunho (RN-005)."""
    return service.criar(db, data)


@router.put("/{id}", response_model=PedidoResponse)
def update(
    id: int,
    data: PedidoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoResponse:
    return service.atualizar(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    """Não aplicável a pedidos com itens fora de Rascunho; usar apenas em Rascunho."""
    service.deletar(db, id)


@router.post("/{id}/submit", response_model=PedidoResponse)
def submit(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoResponse:
    """RTV envia pedido para validação (Rascunho -> Pendente Aprovação). Valida RN-003."""
    return service.submeter(db, id)


@router.post("/{id}/approve", response_model=PedidoResponse)
def approve(
    id: int,
    body: ApproveRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoResponse:
    """Trader aprova o pedido (RN-007). RTV não pode aprovar o próprio pedido (RN-009)."""
    return service.aprovar(db, id, current_user, body)


@router.post("/{id}/reject", response_model=PedidoResponse)
def reject(
    id: int,
    body: RejectRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoResponse:
    """Trader rejeita o pedido (RN-007). Comentário obrigatório (RN-008)."""
    return service.rejeitar(db, id, current_user, body)


@router.post("/{id}/return", response_model=PedidoResponse)
def return_to_author(
    id: int,
    body: ReturnRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PedidoResponse:
    """Trader devolve com questionamento (RN-007). Comentário obrigatório (RN-008).
    Pedido volta a Rascunho (RN-010)."""
    return service.devolver(db, id, current_user, body)
