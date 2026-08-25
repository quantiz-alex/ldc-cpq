from datetime import date, datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.pedido_itens import PedidoItem
from backend.models.pedidos import Pedido
from backend.models.usuarios import Usuario
from backend.repositories import pedidos as repository
from backend.schemas.pedidos import ApproveRequest, PedidoCreate, PedidoUpdate, RejectRequest, ReturnRequest

MSG_PEDIDO_INCOMPLETO = (
    "Pedido incompleto — preencha cliente, ao menos 1 item, quantidade, janela de entrega, "
    "formato de entrega, prazo de pagamento e local de entrega antes de enviar para validação"
)


def listar(
    db: Session,
    current_user: Usuario,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    rtv_id: int | None = None,
    cliente_id: int | None = None,
    data_pedido_de: date | None = None,
    data_pedido_ate: date | None = None,
) -> list[Pedido]:
    """RN-001/RN-015: RTV vê apenas a própria carteira de pedidos; trader/admin veem todos."""
    if current_user.role == "rtv":
        rtv_id = current_user.id
    return repository.get_all(
        db,
        skip=skip,
        limit=limit,
        status=status,
        rtv_id=rtv_id,
        cliente_id=cliente_id,
        data_pedido_de=data_pedido_de,
        data_pedido_ate=data_pedido_ate,
    )


def obter(db: Session, id: int) -> Pedido:
    pedido = repository.get_by_id(db, id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return pedido


def criar(db: Session, data: PedidoCreate) -> Pedido:
    """RN-005: pedido sempre é criado em status Rascunho (nunca dispara approval automaticamente)."""
    return repository.create(db, data)


def atualizar(db: Session, id: int, data: PedidoUpdate) -> Pedido:
    pedido = repository.update(db, id, data)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return pedido


def deletar(db: Session, id: int) -> None:
    pedido = repository.get_by_id(db, id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    if pedido.status != "Rascunho":
        raise HTTPException(
            status_code=422,
            detail="Somente pedidos em Rascunho podem ser excluídos",
        )
    repository.delete(db, id)


def _validar_completude_para_envio(db: Session, pedido: Pedido) -> None:
    """RN-003: valida completude do pedido antes do envio para o trader.

    Exige acesso ao banco (contagem/checagem dos pedido_itens vinculados), o que não é
    possível em um model_validator Pydantic stateless — por isso a checagem real vive aqui,
    no service, disparada pela ação de workflow POST /pedidos/{id}/submit (que não tem corpo
    de requisição a validar via schema).
    """
    if pedido.cliente_id is None:
        raise HTTPException(status_code=422, detail=MSG_PEDIDO_INCOMPLETO)

    itens = db.query(PedidoItem).filter(PedidoItem.pedido_id == pedido.id).all()
    if len(itens) < 1:
        raise HTTPException(status_code=422, detail=MSG_PEDIDO_INCOMPLETO)

    campos_obrigatorios = (
        "quantidade",
        "janela_mes",
        "janela_ano",
        "formato_entrega",
        "condicao_pagamento",
        "local_entrega",
    )
    for item in itens:
        for campo in campos_obrigatorios:
            valor = getattr(item, campo)
            if valor is None or (isinstance(valor, str) and len(valor.strip()) == 0):
                raise HTTPException(status_code=422, detail=MSG_PEDIDO_INCOMPLETO)


def submeter(db: Session, id: int) -> Pedido:
    """POST /pedidos/{id}/submit — RTV envia pedido para validação (Rascunho -> Pendente Aprovação).
    Valida RN-003 (completude) antes da transição de status.
    """
    pedido = obter(db, id)
    _validar_completude_para_envio(db, pedido)
    pedido.status = "Pendente Aprovação"
    db.commit()
    db.refresh(pedido)
    return pedido


def aprovar(db: Session, id: int, current_user: Usuario, body: ApproveRequest) -> Pedido:
    """POST /pedidos/{id}/approve — RN-007 (somente trader/admin), RN-009 (RTV não aprova o
    próprio pedido). Pedido só entra na contagem de receita do dashboard após esta ação (RN-002).
    """
    pedido = obter(db, id)
    if current_user.role not in ("trader", "admin"):
        raise HTTPException(
            status_code=403, detail="Somente trader e admin podem aprovar pedidos"
        )
    if current_user.id == pedido.rtv_id:
        raise HTTPException(
            status_code=403, detail="RTV não pode aprovar seus próprios pedidos"
        )
    pedido.status = "Aprovado"
    pedido.aprovado_por = current_user.nome
    pedido.aprovado_em = datetime.now(timezone.utc)
    pedido.comentario_aprovacao = body.comentario
    db.commit()
    db.refresh(pedido)
    return pedido


def rejeitar(db: Session, id: int, current_user: Usuario, body: RejectRequest) -> Pedido:
    """POST /pedidos/{id}/reject — RN-007 (somente trader/admin); comentário obrigatório (RN-008,
    já validado em schemas/pedidos.py::RejectRequest).
    """
    pedido = obter(db, id)
    if current_user.role not in ("trader", "admin"):
        raise HTTPException(
            status_code=403, detail="Somente trader e admin podem rejeitar pedidos"
        )
    pedido.status = "Rejeitado"
    pedido.aprovado_por = current_user.nome
    pedido.aprovado_em = datetime.now(timezone.utc)
    pedido.comentario_aprovacao = body.comentario
    db.commit()
    db.refresh(pedido)
    return pedido


def devolver(db: Session, id: int, current_user: Usuario, body: ReturnRequest) -> Pedido:
    """POST /pedidos/{id}/return — RN-007 (somente trader/admin); comentário obrigatório (RN-008);
    pedido volta a Rascunho (RN-010).
    """
    pedido = obter(db, id)
    if current_user.role not in ("trader", "admin"):
        raise HTTPException(
            status_code=403, detail="Somente trader e admin podem devolver pedidos"
        )
    pedido.status = "Rascunho"
    pedido.aprovado_por = current_user.nome
    pedido.aprovado_em = datetime.now(timezone.utc)
    pedido.comentario_aprovacao = body.comentario
    db.commit()
    db.refresh(pedido)
    return pedido
