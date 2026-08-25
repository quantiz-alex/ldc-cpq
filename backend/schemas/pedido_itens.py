from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, model_validator


class PedidoItemBase(BaseModel):
    pedido_id: int
    produto_id: int
    quantidade: float = Field(..., gt=0)
    unidade: str = Field(..., min_length=1, max_length=20)
    janela_mes: int = Field(..., ge=1, le=12)
    janela_ano: int
    formato_entrega: str = Field(..., min_length=1, max_length=50)
    local_entrega: str = Field(..., min_length=1, max_length=150)
    condicao_pagamento: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Chave de lookup em precos_por_janela junto com produto_id+janela_mes+janela_ano (RN-004)",
    )


class PedidoItemCreate(PedidoItemBase):
    # RN-006: valor de referência da UI (não persistido no modelo) usado para validar que a soma
    # das linhas parceladas do mesmo item (mesmo pedido_id + produto_id) reconstitui a quantidade
    # total configurada pelo RTV na tela de Captação de Pedido ao dividir a entrega por janela.
    #
    # NÃO usar Field(exclude=True) aqui: isso removeria o campo de model_dump(), impedindo que
    # backend/services/pedido_itens.py::criar() o repasse na revalidação com contexto de DB (o
    # validator abaixo ficaria sempre em no-op). A exclusão do campo antes da persistência é
    # feita explicitamente no service via model_dump(exclude={"quantidade_total_esperada"}).
    quantidade_total_esperada: float | None = Field(
        None,
        description="Quantidade total do item (referência de UI para parcelamento) — não persistida",
    )

    # RN-006: a soma das quantidades parceladas por janela deve ser igual à quantidade total do item.
    #
    # A checagem real precisa somar as linhas-irmãs (mesmo pedido_id + produto_id) já persistidas
    # no banco — um model_validator Pydantic puro não tem acesso a uma sessão de DB. Por isso,
    # assim como em UsuarioCreate (RN-017), este validator só executa a soma quando o contexto de
    # validação inclui `db` — o parsing automático do FastAPI (`data: PedidoItemCreate`) não fornece
    # esse contexto; `backend/services/pedido_itens.py::criar()` faz a revalidação explícita com
    # `context={"db": db}` antes de persistir, para garantir que a regra seja de fato aplicada
    # sempre que `quantidade_total_esperada` for informado pelo cliente.
    @model_validator(mode="after")
    def validar_soma_parcelada(self, info: ValidationInfo) -> "PedidoItemCreate":
        ctx = info.context or {}
        db = ctx.get("db")
        if db is not None and self.quantidade_total_esperada is not None:
            from sqlalchemy import func as sa_func

            from backend.models.pedido_itens import PedidoItem

            soma_existente = (
                db.query(sa_func.coalesce(sa_func.sum(PedidoItem.quantidade), 0))
                .filter(
                    PedidoItem.pedido_id == self.pedido_id,
                    PedidoItem.produto_id == self.produto_id,
                )
                .scalar()
            )
            soma_total = float(soma_existente) + float(self.quantidade)
            if round(soma_total, 2) != round(float(self.quantidade_total_esperada), 2):
                raise ValueError(
                    "A soma das quantidades parceladas por janela deve ser igual à quantidade total do item"
                )
        return self


class PedidoItemUpdate(BaseModel):
    quantidade: float | None = Field(None, gt=0)
    janela_mes: int | None = Field(None, ge=1, le=12)
    janela_ano: int | None = None
    formato_entrega: str | None = Field(None, max_length=50)
    local_entrega: str | None = Field(None, max_length=150)
    condicao_pagamento: str | None = Field(None, max_length=50)
    # Ver nota em PedidoItemCreate — sem exclude=True para não ser descartado em model_dump()
    # durante a revalidação com contexto de DB feita por backend/services/pedido_itens.py::atualizar().
    quantidade_total_esperada: float | None = None

    @model_validator(mode="after")
    def validar_soma_parcelada(self, info: ValidationInfo) -> "PedidoItemUpdate":
        ctx = info.context or {}
        db = ctx.get("db")
        pedido_id = ctx.get("pedido_id")
        produto_id = ctx.get("produto_id")
        item_id = ctx.get("item_id")
        if db is not None and self.quantidade_total_esperada is not None and self.quantidade is not None:
            from sqlalchemy import func as sa_func

            from backend.models.pedido_itens import PedidoItem

            query = db.query(sa_func.coalesce(sa_func.sum(PedidoItem.quantidade), 0)).filter(
                PedidoItem.pedido_id == pedido_id, PedidoItem.produto_id == produto_id
            )
            if item_id is not None:
                query = query.filter(PedidoItem.id != item_id)
            soma_existente = query.scalar()
            soma_total = float(soma_existente) + float(self.quantidade)
            if round(soma_total, 2) != round(float(self.quantidade_total_esperada), 2):
                raise ValueError(
                    "A soma das quantidades parceladas por janela deve ser igual à quantidade total do item"
                )
        return self


class PedidoItemResponse(PedidoItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    preco_unitario: float
    subtotal: float
    created_at: datetime
    updated_at: datetime
