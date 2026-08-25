from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.usuarios import Usuario
from backend.schemas.recomendacoes import RecomendacaoCreate, RecomendacaoResponse, RecomendacaoUpdate
from backend.services import recomendacoes as service

router = APIRouter(prefix="/recomendacoes", tags=["Recomendacoes"])


@router.get("/", response_model=list[RecomendacaoResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    cliente_id: int | None = None,
    produto_id: int | None = None,
    motivo: str | None = None,
    aceita: bool | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[RecomendacaoResponse]:
    """RTV só vê recomendações dos clientes de sua carteira (RN-014)."""
    return service.listar(
        db, current_user, skip=skip, limit=limit, cliente_id=cliente_id, produto_id=produto_id,
        motivo=motivo, aceita=aceita,
    )


@router.get("/{id}", response_model=RecomendacaoResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> RecomendacaoResponse:
    return service.obter(db, id)


@router.post("/", response_model=RecomendacaoResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: RecomendacaoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> RecomendacaoResponse:
    """Gerado automaticamente pelo motor de score (RN-013) — nunca cria pedido (RN-012)."""
    return service.criar(db, data)


@router.put("/{id}", response_model=RecomendacaoResponse)
def update(
    id: int,
    data: RecomendacaoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> RecomendacaoResponse:
    """Usado para marcar aceita=true quando o RTV adiciona a sugestão ao pedido."""
    return service.atualizar(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    service.deletar(db, id)
