from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.clientes import Cliente
from backend.models.usuarios import Usuario
from backend.repositories import clientes as repository
from backend.schemas.clientes import ClienteCreate, ClienteUpdate


def listar(
    db: Session,
    current_user: Usuario,
    skip: int = 0,
    limit: int = 100,
    regiao: str | None = None,
    rtv_id: int | None = None,
) -> list[Cliente]:
    """RN-001: RTV só vê a própria carteira de clientes; trader/admin veem todos."""
    if current_user.role == "rtv":
        rtv_id = current_user.id
    return repository.get_all(db, skip=skip, limit=limit, regiao=regiao, rtv_id=rtv_id)


def obter(db: Session, id: int) -> Cliente:
    cliente = repository.get_by_id(db, id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return cliente


def criar(db: Session, data: ClienteCreate) -> Cliente:
    return repository.create(db, data)


def atualizar(db: Session, id: int, data: ClienteUpdate) -> Cliente:
    cliente = repository.update(db, id, data)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return cliente


def deletar(db: Session, id: int) -> None:
    if not repository.delete(db, id):
        raise HTTPException(status_code=404, detail="Registro não encontrado")
