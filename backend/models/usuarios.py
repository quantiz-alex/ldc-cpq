from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from backend.database import Base


class Usuario(Base):
    """Usuários do sistema com autenticação JWT (RTV, trader, admin)."""

    __tablename__ = "usuarios"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False)
    email: str = Column(String(150), nullable=False, unique=True, index=True)
    senha_hash: str = Column(String(255), nullable=False)
    role: str = Column(String(20), nullable=False, index=True)
    rtv_territorio: str | None = Column(String(100), nullable=True)
    ativo: bool = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    clientes = relationship(
        "Cliente", back_populates="rtv", foreign_keys="Cliente.rtv_id"
    )
    pedidos = relationship(
        "Pedido", back_populates="rtv", foreign_keys="Pedido.rtv_id"
    )
