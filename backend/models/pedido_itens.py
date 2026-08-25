from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from backend.database import Base


class PedidoItem(Base):
    """Item do pedido, incluindo o parcelamento da entrega por janela."""

    __tablename__ = "pedido_itens"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pedido_id: int = Column(Integer, ForeignKey("pedidos.id"), nullable=False, index=True)
    produto_id: int = Column(Integer, ForeignKey("produtos.id"), nullable=False, index=True)
    quantidade = Column(Numeric(15, 2), nullable=False)
    unidade: str = Column(String(20), nullable=False)
    janela_mes: int = Column(Integer, nullable=False)
    janela_ano: int = Column(Integer, nullable=False)
    formato_entrega: str = Column(String(50), nullable=False)
    local_entrega: str = Column(String(150), nullable=False)
    condicao_pagamento: str = Column(String(50), nullable=False)
    preco_unitario = Column(Numeric(15, 2), nullable=False)
    subtotal = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="pedido_itens")
