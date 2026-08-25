from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.auth import hash_password
from backend.models.usuarios import Usuario
from backend.repositories import usuarios as repository
from backend.schemas.usuarios import UsuarioCreate, UsuarioUpdate


def listar(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    return repository.get_all(db, skip=skip, limit=limit)


def obter(db: Session, id: int) -> Usuario:
    usuario = repository.get_by_id(db, id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return usuario


def criar(db: Session, data: UsuarioCreate) -> Usuario:
    """RN-017: revalida o schema com contexto de DB para aplicar a checagem real de
    unicidade de e-mail (ver backend/schemas/usuarios.py::UsuarioCreate.validar_email_unico).
    """
    try:
        UsuarioCreate.model_validate(data.model_dump(), context={"db": db})
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()[0]["msg"]) from exc

    senha_hash = hash_password(data.password)
    return repository.create(db, data, senha_hash=senha_hash)


def atualizar(db: Session, id: int, data: UsuarioUpdate) -> Usuario:
    """RN-017: revalida o schema com contexto de DB (excluindo o próprio id) para aplicar a
    checagem real de unicidade de e-mail na edição.
    """
    try:
        UsuarioUpdate.model_validate(
            data.model_dump(exclude_unset=True), context={"db": db, "usuario_id": id}
        )
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()[0]["msg"]) from exc

    usuario = repository.update(db, id, data)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return usuario


def deletar(db: Session, id: int) -> None:
    if not repository.delete(db, id):
        raise HTTPException(status_code=404, detail="Registro não encontrado")
