from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from backend.database import Base


class Recomendacao(Base):
    """Sugestão de produto gerada para um cliente com base em histórico e sazonalidade."""

    __tablename__ = "recomendacoes"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id: int = Column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)
    produto_id: int = Column(Integer, ForeignKey("produtos.id"), nullable=False, index=True)
    motivo: str = Column(String(20), nullable=False)
    score = Column(Numeric(8, 4), nullable=False)
    aceita: bool = Column(Boolean, nullable=False, default=False)
    gerada_em = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    cliente = relationship("Cliente", back_populates="recomendacoes")
    produto = relationship("Produto", back_populates="recomendacoes")
