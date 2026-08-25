from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.usuarios import Usuario
from backend.schemas.precos_por_janela import (
    PrecoLookupResponse,
    PrecoPorJanelaCreate,
    PrecoPorJanelaResponse,
    PrecoPorJanelaUpdate,
)
from backend.services import precos_por_janela as service

router = APIRouter(prefix="/precos-por-janela", tags=["PrecosPorJanela"])


@router.get("/", response_model=list[PrecoPorJanelaResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    produto_id: int | None = None,
    janela_mes: int | None = None,
    janela_ano: int | None = None,
    condicao_pagamento: str | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[PrecoPorJanelaResponse]:
    return service.listar(
        db,
        skip=skip,
        limit=limit,
        produto_id=produto_id,
        janela_mes=janela_mes,
        janela_ano=janela_ano,
        condicao_pagamento=condicao_pagamento,
    )


@router.get("/lookup", response_model=PrecoLookupResponse)
def lookup(
    produto_id: int,
    janela_mes: int,
    janela_ano: int,
    condicao_pagamento: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PrecoLookupResponse:
    """RN-004: lookup do preço vigente por produto + janela + condição comercial —
    usado pela Captação de Pedido para precificação automática, não persiste."""
    return service.lookup(db, produto_id, janela_mes, janela_ano, condicao_pagamento)


@router.get("/{id}", response_model=PrecoPorJanelaResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PrecoPorJanelaResponse:
    return service.obter(db, id)


@router.post("/", response_model=PrecoPorJanelaResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: PrecoPorJanelaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PrecoPorJanelaResponse:
    """Somente admin (RN-016 — manutenção do catálogo/preços)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para esta operação")
    return service.criar(db, data)


@router.put("/{id}", response_model=PrecoPorJanelaResponse)
def update(
    id: int,
    data: PrecoPorJanelaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PrecoPorJanelaResponse:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para esta operação")
    return service.atualizar(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para esta operação")
    service.deletar(db, id)
