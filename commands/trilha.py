"""
Comando: trilha

Exibe o plano de estudos completo de um tema escolhido.

Uso:
    python src/main.py trilha --tema lgpd
    python src/main.py trilha --listar
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import click
from src.services import get_trilha, list_categorias, list_trilhas
from src.utils import list_available_temas


def _exibir_trilha(trilha) -> None:
    """Formata e exibe uma trilha no terminal."""
    separador = "─" * 60

    click.echo()
    click.echo(f"{'═' * 60}")
    click.echo(f"  📚  {trilha.titulo.upper()}")
    click.echo(f"{'═' * 60}")
    click.echo(f"  {trilha.descricao}")
    click.echo(f"  ⏱  Duração estimada: {trilha.duracao_estimada}")
    click.echo(f"{'═' * 60}")
    click.echo()

    for modulo in trilha.modulos:
        click.echo(f"  MÓDULO {modulo.ordem}: {modulo.titulo}")
        click.echo(f"  {separador}")
        click.echo(f"  🎯 Objetivo: {modulo.objetivo}")
        click.echo()

        click.echo("  📌 Tópicos:")
        for topico in modulo.topicos:
            click.echo(f"     • {topico}")
        click.echo()

        click.echo("  📖 Recursos:")
        for recurso in modulo.recursos:
            click.echo(f"     → {recurso}")
        click.echo()

    click.echo(f"{'═' * 60}")
    click.echo("  ✅ Trilha carregada com sucesso!")
    click.echo(f"{'═' * 60}\n")


@click.command()
@click.option(
    "--tema",
    "-t",
    default=None,
    help="Tema da trilha (ex: lgpd, compliance, etica_profissional).",
)
@click.option(
    "--listar",
    "-l",
    is_flag=True,
    default=False,
    help="Lista todas as trilhas disponíveis.",
)
def cmd_trilha(tema: str, listar: bool):
    """Exibe o plano de estudos de um tema escolhido."""

    if listar:
        click.echo("\n  📋 TRILHAS DISPONÍVEIS\n")
        categorias = list_categorias()
        for cat in categorias:
            click.echo(f"  {cat.icone}  {cat.id:<30} {cat.nome}")
        click.echo()
        return

    if not tema:
        temas_disponiveis = list_available_temas()
        click.echo("\n  ⚠️  Informe um tema com --tema.")
        click.echo(f"\n  Temas disponíveis: {', '.join(temas_disponiveis)}")
        click.echo("  Use --listar para ver todos os detalhes.\n")
        return

    trilha = get_trilha(tema)

    if not trilha:
        temas_disponiveis = list_available_temas()
        click.echo(f"\n  ❌ Tema '{tema}' não encontrado.")
        click.echo(f"  Temas disponíveis: {', '.join(temas_disponiveis)}\n")
        return

    _exibir_trilha(trilha)
