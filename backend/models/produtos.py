from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from backend.database import Base


class Produto(Base):
    """SKU de defensivo ou fertilizante do catálogo da LDC."""

    __tablename__ = "produtos"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_comercial: str = Column(String(150), nullable=False)
    tipo: str = Column(String(20), nullable=False, index=True)
    classe: str | None = Column(String(80), nullable=True)
    ingrediente_ativo: str | None = Column(String(150), nullable=True)
    unidade: str = Column(String(20), nullable=False)
    custo = Column(Numeric(15, 2), nullable=False)
    ativo: bool = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    precos_por_janela = relationship("PrecoPorJanela", back_populates="produto")
    pedido_itens = relationship("PedidoItem", back_populates="produto")
    recomendacoes = relationship("Recomendacao", back_populates="produto")
