"""
Ethics Explorer — Ferramentas MCP.

Define as tools expostas pelo servidor MCP do Ethics Explorer.
Cada tool mapeia diretamente para um serviço em src/services.py.

Referência: Model Context Protocol (MCP) — https://modelcontextprotocol.io
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ---------------------------------------------------------------------------
# NOTA: Este módulo está preparado para integração com o SDK oficial do MCP.
# Para ativar, instale: pip install mcp
# e descomente as importações abaixo.
# ---------------------------------------------------------------------------

# from mcp.server import Server
# from mcp.types import Tool, TextContent

from src.services import (
    generate_certificado,
    get_desafio_aleatorio,
    get_desafios,
    get_trilha,
    list_categorias,
    list_trilhas,
)


# ---------------------------------------------------------------------------
# Definições das tools MCP
# ---------------------------------------------------------------------------

TOOLS_SCHEMA = [
    {
        "name": "get_trilha",
        "description": "Retorna o plano de estudos completo de um tema de ética e compliance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tema": {
                    "type": "string",
                    "description": (
                        "ID do tema. Valores aceitos: etica_profissional, compliance, "
                        "lgpd, seguranca_informacao, conduta_organizacional, combate_corrupcao."
                    ),
                }
            },
            "required": ["tema"],
        },
    },
    {
        "name": "list_trilhas",
        "description": "Lista todas as trilhas de estudo disponíveis na plataforma.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_desafio",
        "description": "Gera um desafio de conhecimento por tema e nível de dificuldade.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tema": {
                    "type": "string",
                    "description": "ID do tema (ex: lgpd, compliance).",
                },
                "nivel": {
                    "type": "string",
                    "enum": ["iniciante", "intermediario", "avancado"],
                    "description": "Nível de dificuldade do desafio.",
                },
                "aleatorio": {
                    "type": "boolean",
                    "description": "Se true, retorna um desafio aleatório do tema/nível informado.",
                    "default": False,
                },
            },
            "required": ["tema", "nivel"],
        },
    },
    {
        "name": "generate_certificado",
        "description": "Gera um certificado fictício de conclusão de trilha para o participante.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "description": "Nome completo do participante.",
                },
                "tema": {
                    "type": "string",
                    "description": "ID do tema da trilha concluída.",
                },
            },
            "required": ["nome", "tema"],
        },
    },
    {
        "name": "list_categorias",
        "description": "Lista todas as categorias temáticas disponíveis na plataforma.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]


# ---------------------------------------------------------------------------
# Handlers das tools
# ---------------------------------------------------------------------------

def handle_tool_call(tool_name: str, arguments: dict) -> dict:
    """
    Executa uma tool MCP pelo nome e retorna o resultado.

    Args:
        tool_name: Nome da tool a executar.
        arguments: Argumentos da chamada.

    Returns:
        Dicionário com o resultado da execução.
    """
    if tool_name == "get_trilha":
        tema = arguments.get("tema", "")
        trilha = get_trilha(tema)
        if not trilha:
            return {"error": f"Trilha para o tema '{tema}' não encontrada."}
        return {
            "id": trilha.id,
            "titulo": trilha.titulo,
            "descricao": trilha.descricao,
            "duracao_estimada": trilha.duracao_estimada,
            "modulos": [
                {
                    "ordem": m.ordem,
                    "titulo": m.titulo,
                    "objetivo": m.objetivo,
                    "topicos": m.topicos,
                    "recursos": m.recursos,
                }
                for m in trilha.modulos
            ],
        }

    elif tool_name == "list_trilhas":
        trilhas = list_trilhas()
        return {
            "trilhas": [
                {
                    "id": t.id,
                    "categoria": t.categoria,
                    "titulo": t.titulo,
                    "descricao": t.descricao,
                    "duracao_estimada": t.duracao_estimada,
                }
                for t in trilhas
            ]
        }

    elif tool_name == "get_desafio":
        tema = arguments.get("tema", "")
        nivel = arguments.get("nivel", "iniciante")
        aleatorio = arguments.get("aleatorio", False)

        if aleatorio:
            desafio = get_desafio_aleatorio(tema=tema, nivel=nivel)
        else:
            desafios = get_desafios(tema, nivel)
            desafio = desafios[0] if desafios else None

        if not desafio:
            return {"error": f"Nenhum desafio encontrado para tema='{tema}' e nível='{nivel}'."}

        return {
            "id": desafio.id,
            "categoria": desafio.categoria,
            "nivel": desafio.nivel,
            "pergunta": desafio.pergunta,
            "alternativas": desafio.alternativas,
            "resposta_correta": desafio.resposta_correta,
            "explicacao": desafio.explicacao,
        }

    elif tool_name == "generate_certificado":
        nome = arguments.get("nome", "")
        tema = arguments.get("tema", "")
        certificado = generate_certificado(nome, tema)
        if not certificado:
            return {"error": f"Não foi possível gerar certificado para o tema '{tema}'."}
        return {
            "nome_participante": certificado.nome_participante,
            "titulo_trilha": certificado.titulo_trilha,
            "data_emissao": certificado.data_emissao,
            "codigo_verificacao": certificado.codigo_verificacao,
            "caminho_arquivo": certificado.caminho_arquivo,
        }

    elif tool_name == "list_categorias":
        categorias = list_categorias()
        return {
            "categorias": [
                {
                    "id": c.id,
                    "nome": c.nome,
                    "descricao": c.descricao,
                    "nivel_minimo": c.nivel_minimo,
                    "icone": c.icone,
                }
                for c in categorias
            ]
        }

    else:
        return {"error": f"Tool '{tool_name}' não encontrada."}
