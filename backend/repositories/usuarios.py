from sqlalchemy.orm import Session

from backend.models.usuarios import Usuario
from backend.schemas.usuarios import UsuarioCreate, UsuarioUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    return (
        db.query(Usuario)
        .filter(Usuario.ativo == True)  # noqa: E712
        .order_by(Usuario.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_by_id(db: Session, id: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == id).first()


def get_by_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def create(db: Session, data: UsuarioCreate, senha_hash: str) -> Usuario:
    payload = data.model_dump(exclude={"password"})
    usuario = Usuario(**payload, senha_hash=senha_hash)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def update(db: Session, id: int, data: UsuarioUpdate) -> Usuario | None:
    usuario = get_by_id(db, id)
    if usuario is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(usuario, field, value)
    db.commit()
    db.refresh(usuario)
    return usuario


def delete(db: Session, id: int) -> bool:
    usuario = get_by_id(db, id)
    if usuario is None:
        return False
    usuario.ativo = False
    db.commit()
    return True
