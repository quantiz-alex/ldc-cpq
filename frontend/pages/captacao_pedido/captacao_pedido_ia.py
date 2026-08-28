"""Extração por IA (Captura Assistida) — RN-005.

Lê texto colado (WhatsApp/e-mail) e/ou uma imagem anexada (print de conversa,
e-mail) e devolve SUGESTÕES de cabeçalho (cliente, cultura/safra) e itens
(produto, quantidade, unidade) para o RTV revisar. Não grava nada em CSV —
quem persiste é sempre o chamador (captacao_pedido_callbacks.py /
captacao_pedido_queries.py), e itens sugeridos só viram pedido_itens quando o
RTV confirma manualmente via "Adicionar Item" (RN-003/RN-004 inalteradas).
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

from frontend.pages.captacao_pedido.captacao_pedido_queries import (
    opcoes_clientes,
    opcoes_produtos,
)

load_dotenv()

_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

_TOOL_NAME = "registrar_extracao_pedido"

_TOOL_SCHEMA = {
    "name": _TOOL_NAME,
    "description": (
        "Registra os dados extraídos de uma mensagem de cliente (texto e/ou "
        "imagem) para pré-preenchimento de um rascunho de pedido."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "cliente_id": {
                "type": ["integer", "null"],
                "description": (
                    "id do cliente da lista fornecida cujo nome bate com quem "
                    "está pedindo, ou null se não for possível identificar com "
                    "confiança."
                ),
            },
            "cultura_safra": {
                "type": ["string", "null"],
                "description": "Cultura/safra mencionada (ex: 'Soja 24/25'), ou null.",
            },
            "itens": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "produto_id": {
                            "type": ["integer", "null"],
                            "description": (
                                "id do produto da lista fornecida que melhor "
                                "corresponde ao item mencionado, ou null se "
                                "nenhum produto do catálogo corresponder."
                            ),
                        },
                        "produto_nome_extraido": {
                            "type": "string",
                            "description": "Nome do produto exatamente como mencionado na mensagem.",
                        },
                        "quantidade": {"type": ["number", "null"]},
                        "unidade": {"type": ["string", "null"]},
                    },
                    "required": ["produto_nome_extraido"],
                },
            },
            "resumo": {
                "type": "string",
                "description": (
                    "Resumo curto (1-3 frases) do pedido para auditoria, em "
                    "português."
                ),
            },
        },
        "required": ["itens", "resumo"],
    },
}


def _montar_prompt_catalogo() -> str:
    clientes = "\n".join(f"- id={c['value']}: {c['label']}" for c in opcoes_clientes())
    produtos = "\n".join(f"- id={p['value']}: {p['label']}" for p in opcoes_produtos())
    return (
        "Você está extraindo dados de uma mensagem recebida de um cliente "
        "(WhatsApp, e-mail ou print) para pré-preencher um rascunho de pedido "
        "num sistema de CPQ agrícola. Use SOMENTE os ids das listas abaixo — "
        "nunca invente um id que não esteja listado. Se não tiver certeza de "
        "qual cliente ou produto corresponde, deixe o id como null em vez de "
        "adivinhar.\n\n"
        f"Clientes ativos:\n{clientes or '(nenhum cadastrado)'}\n\n"
        f"Produtos ativos:\n{produtos or '(nenhum cadastrado)'}\n\n"
        "Não invente condições comerciais (prazo de pagamento, formato de "
        "entrega, local de entrega, janela de entrega) que não estejam "
        "explícitas na mensagem — isso é preenchido manualmente depois."
    )


def extrair_pedido_de_mensagem(
    texto: str | None,
    imagem_base64: str | None,
    imagem_media_type: str | None,
) -> tuple[bool, dict | None, str]:
    """Chama o Claude para extrair cabeçalho/itens sugeridos.

    Retorna (sucesso, resultado, mensagem_erro). `resultado` segue o schema de
    `_TOOL_SCHEMA["input_schema"]` quando sucesso=True.
    """
    if not texto and not imagem_base64:
        return False, None, "Cole o texto da mensagem e/ou anexe uma imagem antes de gerar o rascunho."

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return False, None, (
            "IA de captura assistida não configurada — defina ANTHROPIC_API_KEY "
            "no ambiente do servidor."
        )

    conteudo: list[dict] = []
    if imagem_base64:
        conteudo.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": imagem_media_type or "image/png",
                    "data": imagem_base64,
                },
            }
        )
    conteudo.append(
        {
            "type": "text",
            "text": texto or "(sem texto colado — extraia a partir da imagem anexada)",
        }
    )

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        resposta = client.messages.create(
            model=_MODEL,
            max_tokens=2048,
            system=_montar_prompt_catalogo(),
            tools=[_TOOL_SCHEMA],
            tool_choice={"type": "tool", "name": _TOOL_NAME},
            messages=[{"role": "user", "content": conteudo}],
        )
    except Exception as exc:  # falha de rede, timeout, chave inválida, etc.
        return False, None, f"Falha ao chamar a IA de captura assistida: {exc}"

    for bloco in resposta.content:
        if getattr(bloco, "type", None) == "tool_use" and bloco.name == _TOOL_NAME:
            try:
                return True, dict(bloco.input), ""
            except (TypeError, ValueError) as exc:
                return False, None, f"Resposta da IA em formato inesperado: {exc}"

    return False, None, "A IA não retornou uma extração estruturada — tente novamente."
