from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.clientes import Cliente
from backend.models.recomendacoes import Recomendacao
from backend.models.usuarios import Usuario
from backend.repositories import recomendacoes as repository
from backend.schemas.recomendacoes import RecomendacaoCreate, RecomendacaoUpdate


def listar(
    db: Session,
    current_user: Usuario,
    skip: int = 0,
    limit: int = 100,
    cliente_id: int | None = None,
    produto_id: int | None = None,
    motivo: str | None = None,
    aceita: bool | None = None,
) -> list[Recomendacao]:
    """RN-014: RTV só vê recomendações dos clientes de sua carteira."""
    query_recomendacoes = repository.get_all(
        db, skip=skip, limit=limit, cliente_id=cliente_id, produto_id=produto_id, motivo=motivo, aceita=aceita
    )
    if current_user.role == "rtv":
        ids_clientes_da_carteira = {
            c.id for c in db.query(Cliente).filter(Cliente.rtv_id == current_user.id).all()
        }
        query_recomendacoes = [r for r in query_recomendacoes if r.cliente_id in ids_clientes_da_carteira]
    return query_recomendacoes


def obter(db: Session, id: int) -> Recomendacao:
    recomendacao = repository.get_by_id(db, id)
    if recomendacao is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return recomendacao


def criar(db: Session, data: RecomendacaoCreate) -> Recomendacao:
    """RN-013: score é gerado pelo motor de recomendação (recência + frequência + volume
    histórico + sazonalidade). docs/business_logic.yaml marca RN-013 como `parsed: false`
    (pesos/fórmula de combinação não detalhados no roadmap) — por isso o cálculo do score
    NÃO é implementado aqui como fórmula; o valor chega já calculado no payload
    (`RecomendacaoCreate.score`), a ser substituído por um serviço de scoring real
    (ex.: backend/services/motor_recomendacao.py) quando RN-013 for detalhada no roadmap.
    """
    return repository.create(db, data)


def atualizar(db: Session, id: int, data: RecomendacaoUpdate) -> Recomendacao:
    """RN-012: recomendação nunca cria pedido automaticamente — marcar aceita=true aqui é
    apenas o registro da decisão; a criação do pedido_itens correspondente é uma ação
    explícita separada do RTV na tela de Captação de Pedido (fora deste endpoint)."""
    recomendacao = repository.update(db, id, data)
    if recomendacao is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return recomendacao


def deletar(db: Session, id: int) -> None:
    if not repository.delete(db, id):
        raise HTTPException(status_code=404, detail="Registro não encontrado")
