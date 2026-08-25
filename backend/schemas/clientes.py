from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=150)
    documento: str = Field(..., min_length=1, max_length=20)
    regiao: str = Field(..., min_length=1, max_length=100)
    cultura_principal: str | None = Field(None, max_length=100)
    rtv_id: int


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=150)
    documento: str | None = Field(None, min_length=1, max_length=20)
    regiao: str | None = Field(None, min_length=1, max_length=100)
    cultura_principal: str | None = Field(None, max_length=100)
    rtv_id: int | None = None


class ClienteResponse(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ativo: bool
    created_at: datetime
    updated_at: datetime
