from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from backend.database import Base


class AlertaConsistencia(Base):
    """Registro dos alertas gerados automaticamente na análise do pedido."""

    __tablename__ = "alertas_consistencia"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pedido_id: int = Column(Integer, ForeignKey("pedidos.id"), nullable=False, index=True)
    tipo: str = Column(String(30), nullable=False)
    descricao: str = Column(Text, nullable=False)
    severidade: str = Column(String(10), nullable=False, index=True)
    resolvido_por: str | None = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    pedido = relationship("Pedido", back_populates="alertas")
