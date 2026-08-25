from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

TIPOS_VALIDOS = ("ProdutoAtipico", "VolumetriaAtipica", "CondicaoDivergente")
SEVERIDADES_VALIDAS = ("Baixa", "Media", "Alta")


class AlertaConsistenciaBase(BaseModel):
    pedido_id: int
    tipo: str = Field(..., description="ProdutoAtipico | VolumetriaAtipica | CondicaoDivergente")
    descricao: str = Field(..., min_length=1)
    severidade: str = Field(..., description="Baixa | Media | Alta")

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        if v not in TIPOS_VALIDOS:
            raise ValueError(f"tipo deve ser um de: {', '.join(TIPOS_VALIDOS)}")
        return v

    @field_validator("severidade")
    @classmethod
    def validar_severidade(cls, v: str) -> str:
        if v not in SEVERIDADES_VALIDAS:
            raise ValueError(f"severidade deve ser uma de: {', '.join(SEVERIDADES_VALIDAS)}")
        return v


class AlertaConsistenciaCreate(AlertaConsistenciaBase):
    pass


class AlertaConsistenciaUpdate(BaseModel):
    resolvido_por: str | None = Field(None, max_length=100)


class AlertaConsistenciaResponse(AlertaConsistenciaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resolvido_por: str | None = None
    created_at: datetime
    updated_at: datetime
