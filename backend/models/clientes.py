from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from backend.database import Base


class Cliente(Base):
    """Produtor rural ou revenda atendido pela LDC Insumos."""

    __tablename__ = "clientes"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome: str = Column(String(150), nullable=False)
    documento: str = Column(String(20), nullable=False, unique=True, index=True)
    regiao: str = Column(String(100), nullable=False, index=True)
    cultura_principal: str | None = Column(String(100), nullable=True)
    rtv_id: int = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    ativo: bool = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    rtv = relationship("Usuario", back_populates="clientes", foreign_keys=[rtv_id])
    pedidos = relationship("Pedido", back_populates="cliente")
    recomendacoes = relationship("Recomendacao", back_populates="cliente")
