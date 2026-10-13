"""
Ethics Explorer — Ponto de entrada da CLI.

Uso:
    python src/main.py trilha --tema lgpd
    python src/main.py desafio --tema compliance --nivel iniciante
    python src/main.py certificado --nome "João Silva" --tema lgpd
"""

import sys
from pathlib import Path

# Garante que o diretório raiz do projeto está no sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import click
from commands.certificado import cmd_certificado
from commands.desafio import cmd_desafio
from commands.trilha import cmd_trilha


@click.group()
@click.version_option(version="1.0.0", prog_name="Ethics Explorer")
def cli():
    """
    \b
    ╔══════════════════════════════════════╗
    ║         ETHICS EXPLORER  v1.0        ║
    ║  Plataforma de Ética e Compliance    ║
    ╚══════════════════════════════════════╝

    Comandos disponíveis:

    \b
      trilha       Exibe uma trilha de estudos
      desafio      Gera um desafio de conhecimento
      certificado  Emite um certificado de conclusão
    """


cli.add_command(cmd_trilha, name="trilha")
cli.add_command(cmd_desafio, name="desafio")
cli.add_command(cmd_certificado, name="certificado")

if __name__ == "__main__":
    cli()
