from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

TIPOS_VALIDOS = ("Defensivo", "Fertilizante")


class ProdutoBase(BaseModel):
    nome_comercial: str = Field(..., min_length=1, max_length=150)
    tipo: str = Field(..., description="Defensivo | Fertilizante")
    classe: str | None = Field(None, max_length=80)
    ingrediente_ativo: str | None = Field(None, max_length=150)
    unidade: str = Field(..., min_length=1, max_length=20)
    custo: float = Field(..., ge=0)

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        if v not in TIPOS_VALIDOS:
            raise ValueError(f"tipo deve ser um de: {', '.join(TIPOS_VALIDOS)}")
        return v


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome_comercial: str | None = Field(None, min_length=1, max_length=150)
    tipo: str | None = None
    classe: str | None = Field(None, max_length=80)
    ingrediente_ativo: str | None = Field(None, max_length=150)
    unidade: str | None = Field(None, max_length=20)
    custo: float | None = Field(None, ge=0)

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, v: str | None) -> str | None:
        if v is not None and v not in TIPOS_VALIDOS:
            raise ValueError(f"tipo deve ser um de: {', '.join(TIPOS_VALIDOS)}")
        return v


class ProdutoResponse(ProdutoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ativo: bool
    created_at: datetime
    updated_at: datetime
