from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import relationship

from backend.database import Base


class Pedido(Base):
    """Pedido comercial captado pelo RTV, submetido à validação do trader."""

    __tablename__ = "pedidos"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id: int = Column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)
    rtv_id: int = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    cultura_safra: str | None = Column(String(100), nullable=True)
    canal_origem: str = Column(String(20), nullable=False)
    valor_total = Column(Numeric(15, 2), nullable=False, default=0)
    observacoes: str | None = Column(Text, nullable=True)
    status: str = Column(String(30), nullable=False, default="Rascunho", index=True)
    aprovado_por: str | None = Column(String(100), nullable=True)
    aprovado_em = Column(DateTime, nullable=True)
    comentario_aprovacao: str | None = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    cliente = relationship("Cliente", back_populates="pedidos")
    rtv = relationship("Usuario", back_populates="pedidos", foreign_keys=[rtv_id])
    itens = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")
    alertas = relationship("AlertaConsistencia", back_populates="pedido", cascade="all, delete-orphan")
