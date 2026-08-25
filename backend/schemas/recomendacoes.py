from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

MOTIVOS_VALIDOS = ("Historico", "Sazonalidade", "MixRegional")


class RecomendacaoBase(BaseModel):
    cliente_id: int
    produto_id: int
    motivo: str = Field(..., description="Historico | Sazonalidade | MixRegional")

    @field_validator("motivo")
    @classmethod
    def validar_motivo(cls, v: str) -> str:
        if v not in MOTIVOS_VALIDOS:
            raise ValueError(f"motivo deve ser um de: {', '.join(MOTIVOS_VALIDOS)}")
        return v


class RecomendacaoCreate(RecomendacaoBase):
    score: float = Field(..., ge=0)
    gerada_em: datetime


class RecomendacaoUpdate(BaseModel):
    aceita: bool | None = None


class RecomendacaoResponse(RecomendacaoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    score: float
    aceita: bool
    gerada_em: datetime
    created_at: datetime
    updated_at: datetime
