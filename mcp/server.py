"""
Ethics Explorer — Servidor MCP.

Ponto de entrada para o servidor Model Context Protocol (MCP).
Expõe as funcionalidades da plataforma como tools para agentes de IA.

Uso:
    python mcp/server.py

Requisitos:
    pip install mcp  (quando disponível)

Referência: https://modelcontextprotocol.io
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.tools import TOOLS_SCHEMA, handle_tool_call

# ---------------------------------------------------------------------------
# NOTA: A integração completa com o SDK do MCP requer:
#   pip install mcp>=1.0.0
#
# O código abaixo mostra a estrutura esperada para integração com o SDK oficial.
# Quando o SDK estiver disponível, descomente as seções marcadas com [MCP-SDK].
# ---------------------------------------------------------------------------


def run_server_stdio():
    """
    Executa o servidor MCP em modo stdio (padrão para integração com IDEs e agentes).

    O servidor lê requisições JSON do stdin e escreve respostas no stdout,
    seguindo o protocolo MCP.
    """
    # [MCP-SDK] Quando o SDK estiver disponível:
    #
    # from mcp.server import Server
    # from mcp.server.stdio import stdio_server
    # from mcp.types import Tool, TextContent, CallToolResult
    #
    # server = Server("ethics-explorer")
    #
    # @server.list_tools()
    # async def list_tools():
    #     return [Tool(**tool) for tool in TOOLS_SCHEMA]
    #
    # @server.call_tool()
    # async def call_tool(name: str, arguments: dict):
    #     result = handle_tool_call(name, arguments)
    #     return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    #
    # async def main():
    #     async with stdio_server() as streams:
    #         await server.run(*streams)
    #
    # import asyncio
    # asyncio.run(main())

    # Implementação mínima de fallback para testes sem o SDK
    print(json.dumps({"status": "Ethics Explorer MCP Server", "tools": len(TOOLS_SCHEMA)}))
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            tool_name = request.get("tool")
            arguments = request.get("arguments", {})
            result = handle_tool_call(tool_name, arguments)
            print(json.dumps(result, ensure_ascii=False))
            sys.stdout.flush()
        except json.JSONDecodeError:
            print(json.dumps({"error": "Requisição JSON inválida."}))
            sys.stdout.flush()


def get_server_info() -> dict:
    """
    Retorna metadados do servidor MCP.

    Returns:
        Dicionário com nome, versão e tools disponíveis.
    """
    return {
        "name": "ethics-explorer",
        "version": "1.0.0",
        "description": "Plataforma educacional de ética, compliance e conduta organizacional.",
        "tools": [{"name": t["name"], "description": t["description"]} for t in TOOLS_SCHEMA],
    }


if __name__ == "__main__":
    if "--info" in sys.argv:
        print(json.dumps(get_server_info(), ensure_ascii=False, indent=2))
    else:
        run_server_stdio()
