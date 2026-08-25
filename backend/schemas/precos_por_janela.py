from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class PrecoPorJanelaBase(BaseModel):
    produto_id: int
    janela_mes: int = Field(..., ge=1, le=12)
    janela_ano: int
    condicao_pagamento: str = Field(..., min_length=1, max_length=50)
    preco: float = Field(..., ge=0)
    vigente_de: date
    vigente_ate: date | None = None


class PrecoPorJanelaCreate(PrecoPorJanelaBase):
    pass


class PrecoPorJanelaUpdate(BaseModel):
    produto_id: int | None = None
    janela_mes: int | None = Field(None, ge=1, le=12)
    janela_ano: int | None = None
    condicao_pagamento: str | None = Field(None, max_length=50)
    preco: float | None = Field(None, ge=0)
    vigente_de: date | None = None
    vigente_ate: date | None = None


class PrecoPorJanelaResponse(PrecoPorJanelaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class PrecoLookupResponse(BaseModel):
    """Resposta do lookup de preço vigente (RN-004) — não persiste."""

    preco_unitario: float
    vigente_de: date
    vigente_ate: date | None = None
