from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from backend.database import Base


class PrecoPorJanela(Base):
    """Preço vigente de um produto para uma janela de entrega específica."""

    __tablename__ = "precos_por_janela"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    produto_id: int = Column(Integer, ForeignKey("produtos.id"), nullable=False, index=True)
    janela_mes: int = Column(Integer, nullable=False)
    janela_ano: int = Column(Integer, nullable=False)
    condicao_pagamento: str = Column(String(50), nullable=False)
    preco = Column(Numeric(15, 2), nullable=False)
    vigente_de = Column(Date, nullable=False)
    vigente_ate = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    produto = relationship("Produto", back_populates="precos_por_janela")
