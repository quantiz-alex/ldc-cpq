from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.produtos import Produto
from backend.repositories import produtos as repository
from backend.schemas.produtos import ProdutoCreate, ProdutoUpdate


def listar(db: Session, skip: int = 0, limit: int = 100) -> list[Produto]:
    return repository.get_all(db, skip=skip, limit=limit)


def obter(db: Session, id: int) -> Produto:
    produto = repository.get_by_id(db, id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return produto


def criar(db: Session, data: ProdutoCreate) -> Produto:
    return repository.create(db, data)


def atualizar(db: Session, id: int, data: ProdutoUpdate) -> Produto:
    produto = repository.update(db, id, data)
    if produto is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return produto


def deletar(db: Session, id: int) -> None:
    if not repository.delete(db, id):
        raise HTTPException(status_code=404, detail="Registro não encontrado")
