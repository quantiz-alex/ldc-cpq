from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator, model_validator

ROLES_VALIDOS = ("admin", "trader", "rtv")


class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=150, description="Endereço de e-mail único do usuário")
    role: str = Field(..., description="admin | trader | rtv")
    rtv_territorio: str | None = Field(None, max_length=100)

    @field_validator("email")
    @classmethod
    def validar_formato_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Formato de e-mail inválido")
        return v

    @field_validator("role")
    @classmethod
    def validar_role(cls, v: str) -> str:
        if v not in ROLES_VALIDOS:
            raise ValueError(f"role deve ser um de: {', '.join(ROLES_VALIDOS)}")
        return v


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)

    # RN-017: Email deve ser único no sistema.
    #
    # A verificação de unicidade exige uma consulta ao banco (SELECT ... WHERE email = :email),
    # o que um model_validator Pydantic não consegue fazer de forma pura/stateless — schemas não
    # têm acesso a uma sessão de banco de dados. Para contornar isso sem abandonar o padrão
    # "validação declarada no schema", usamos o mecanismo de contexto do Pydantic v2
    # (ValidationInfo.context): quando `context={"db": <Session>}` é fornecido, o validator abaixo
    # executa a checagem real. O parsing automático do FastAPI (`data: UsuarioCreate` no endpoint)
    # NÃO fornece esse contexto, então `backend/services/usuarios.py::criar()` faz uma segunda
    # passada explícita — `UsuarioCreate.model_validate(data.model_dump(), context={"db": db})` —
    # antes de persistir, garantindo que a regra seja sempre aplicada de fato.
    @model_validator(mode="after")
    def validar_email_unico(self, info: ValidationInfo) -> "UsuarioCreate":
        ctx = info.context or {}
        db = ctx.get("db")
        if db is not None:
            from backend.models.usuarios import Usuario

            existente = db.query(Usuario).filter(Usuario.email == self.email).first()
            if existente is not None:
                raise ValueError("Email deve ser único no sistema")
        return self


class UsuarioUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=100)
    email: str | None = Field(None, min_length=3, max_length=150)
    role: str | None = None
    rtv_territorio: str | None = Field(None, max_length=100)

    @field_validator("email")
    @classmethod
    def validar_formato_email(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Formato de e-mail inválido")
        return v

    @field_validator("role")
    @classmethod
    def validar_role(cls, v: str | None) -> str | None:
        if v is not None and v not in ROLES_VALIDOS:
            raise ValueError(f"role deve ser um de: {', '.join(ROLES_VALIDOS)}")
        return v

    # RN-017: mesma regra de unicidade de e-mail, aplicada na edição — ver nota completa em
    # UsuarioCreate.validar_email_unico. Aqui o próprio id do usuário em edição é excluído da
    # comparação (via context["usuario_id"]) para não conflitar com o e-mail já cadastrado dele.
    @model_validator(mode="after")
    def validar_email_unico(self, info: ValidationInfo) -> "UsuarioUpdate":
        ctx = info.context or {}
        db = ctx.get("db")
        usuario_id = ctx.get("usuario_id")
        if db is not None and self.email is not None:
            from backend.models.usuarios import Usuario

            query = db.query(Usuario).filter(Usuario.email == self.email)
            if usuario_id is not None:
                query = query.filter(Usuario.id != usuario_id)
            if query.first() is not None:
                raise ValueError("Email deve ser único no sistema")
        return self


class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ativo: bool
    created_at: datetime
    updated_at: datetime
