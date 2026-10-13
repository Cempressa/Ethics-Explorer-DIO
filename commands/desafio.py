"""
Comando: desafio

Gera desafios de conhecimento por tema e nível de dificuldade.

Uso:
    python src/main.py desafio --tema lgpd --nivel iniciante
    python src/main.py desafio --tema compliance --nivel avancado
    python src/main.py desafio --aleatorio
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import click
from src.services import get_desafio_aleatorio, get_desafios
from src.utils import list_available_niveis, list_available_temas


def _exibir_desafio_interativo(desafio) -> bool:
    """
    Exibe um desafio e aguarda a resposta do usuário.

    Returns:
        True se o usuário acertou, False caso contrário.
    """
    separador = "─" * 60

    click.echo()
    click.echo(f"  {'═' * 58}")
    click.echo(f"  🏷️  Tema: {desafio.categoria.replace('_', ' ').title()}")
    click.echo(f"  📊 Nível: {desafio.nivel.capitalize()}")
    click.echo(f"  {'═' * 58}")
    click.echo()
    click.echo(f"  ❓ {desafio.pergunta}")
    click.echo()

    for alternativa in desafio.alternativas:
        click.echo(f"     {alternativa}")

    click.echo()
    resposta = click.prompt("  Sua resposta (A/B/C/D)").strip().upper()

    click.echo()
    click.echo(f"  {separador}")

    if resposta == desafio.resposta_correta:
        click.echo("  ✅ CORRETO! Muito bem!")
    else:
        click.echo(f"  ❌ INCORRETO. A resposta correta é: {desafio.resposta_correta}")

    click.echo()
    click.echo(f"  💡 Explicação:")
    click.echo(f"  {desafio.explicacao}")
    click.echo(f"  {separador}\n")

    return resposta == desafio.resposta_correta


@click.command()
@click.option(
    "--tema",
    "-t",
    default=None,
    help="Tema do desafio (ex: lgpd, compliance).",
)
@click.option(
    "--nivel",
    "-n",
    default=None,
    type=click.Choice(["iniciante", "intermediario", "avancado"], case_sensitive=False),
    help="Nível de dificuldade.",
)
@click.option(
    "--aleatorio",
    "-a",
    is_flag=True,
    default=False,
    help="Gera um desafio aleatório (tema e nível sorteados).",
)
@click.option(
    "--todos",
    is_flag=True,
    default=False,
    help="Apresenta todos os desafios do tema/nível escolhido em sequência.",
)
def cmd_desafio(tema: str, nivel: str, aleatorio: bool, todos: bool):
    """Gera um desafio de conhecimento por tema e nível."""

    if aleatorio:
        desafio = get_desafio_aleatorio(tema=tema, nivel=nivel)
        if not desafio:
            click.echo("\n  ❌ Nenhum desafio encontrado para os filtros informados.\n")
            return
        _exibir_desafio_interativo(desafio)
        return

    if not tema:
        temas_disponiveis = list_available_temas()
        click.echo("\n  ⚠️  Informe um tema com --tema ou use --aleatorio.")
        click.echo(f"  Temas disponíveis: {', '.join(temas_disponiveis)}\n")
        return

    if not nivel:
        niveis_disponiveis = list_available_niveis()
        click.echo("\n  ⚠️  Informe um nível com --nivel.")
        click.echo(f"  Níveis disponíveis: {', '.join(niveis_disponiveis)}\n")
        return

    desafios = get_desafios(tema, nivel)

    if not desafios:
        click.echo(f"\n  ❌ Nenhum desafio encontrado para tema='{tema}' e nível='{nivel}'.\n")
        return

    if todos:
        acertos = 0
        for desafio in desafios:
            if _exibir_desafio_interativo(desafio):
                acertos += 1
            continuar = click.confirm("  Continuar para o próximo desafio?", default=True)
            if not continuar:
                break

        click.echo(f"\n  🏆 Resultado: {acertos}/{len(desafios)} acertos\n")
    else:
        # Apresenta apenas o primeiro desafio encontrado
        _exibir_desafio_interativo(desafios[0])
