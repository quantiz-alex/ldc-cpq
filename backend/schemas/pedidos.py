from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

CANAIS_VALIDOS = ("WhatsApp", "Email", "Imagem", "Manual")
STATUS_VALIDOS = ("Rascunho", "Pendente Aprovação", "Aprovado", "Rejeitado", "Devolvido")


class PedidoBase(BaseModel):
    cliente_id: int
    rtv_id: int
    cultura_safra: str | None = Field(None, max_length=100)
    canal_origem: str = Field(..., description="WhatsApp | Email | Imagem | Manual")
    observacoes: str | None = None

    @field_validator("canal_origem")
    @classmethod
    def validar_canal_origem(cls, v: str) -> str:
        if v not in CANAIS_VALIDOS:
            raise ValueError(f"canal_origem deve ser um de: {', '.join(CANAIS_VALIDOS)}")
        return v


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(BaseModel):
    cliente_id: int | None = None
    canal_origem: str | None = None
    cultura_safra: str | None = Field(None, max_length=100)
    observacoes: str | None = None

    @field_validator("canal_origem")
    @classmethod
    def validar_canal_origem(cls, v: str | None) -> str | None:
        if v is not None and v not in CANAIS_VALIDOS:
            raise ValueError(f"canal_origem deve ser um de: {', '.join(CANAIS_VALIDOS)}")
        return v


class PedidoResponse(PedidoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    valor_total: float
    status: str
    aprovado_por: str | None = None
    aprovado_em: datetime | None = None
    comentario_aprovacao: str | None = None
    created_at: datetime
    updated_at: datetime


# ── Ações de workflow da Fila de Validação do Trader (RN-007/008/009/010/011) ──────────────


class ApproveRequest(BaseModel):
    comentario: str | None = Field(None, max_length=1000)


class RejectRequest(BaseModel):
    """RN-008: comentário obrigatório para rejeitar o pedido — checagem pura de payload,
    não depende de banco de dados, por isso implementada diretamente como model_validator.
    """

    comentario: str = Field(..., description="Motivo da rejeição — obrigatório (RN-008)")

    @model_validator(mode="after")
    def validar_comentario_obrigatorio(self) -> "RejectRequest":
        if self.comentario is None or len(self.comentario.strip()) == 0:
            raise ValueError("Comentário obrigatório para rejeitar ou devolver o pedido")
        return self


class ReturnRequest(BaseModel):
    """RN-008: comentário obrigatório para devolver o pedido ao autor."""

    comentario: str = Field(..., description="Motivo da devolução — obrigatório (RN-008)")

    @model_validator(mode="after")
    def validar_comentario_obrigatorio(self) -> "ReturnRequest":
        if self.comentario is None or len(self.comentario.strip()) == 0:
            raise ValueError("Comentário obrigatório para rejeitar ou devolver o pedido")
        return self
