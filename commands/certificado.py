"""
Comando: certificado

Gera certificados fictícios de conclusão de trilha.

Uso:
    python src/main.py certificado --nome "Maria Silva" --tema lgpd
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import click
from src.services import generate_certificado
from src.utils import list_available_temas


@click.command()
@click.option(
    "--nome",
    "-n",
    required=True,
    help="Nome completo do participante.",
)
@click.option(
    "--tema",
    "-t",
    required=True,
    help="Tema da trilha concluída (ex: lgpd, compliance).",
)
def cmd_certificado(nome: str, tema: str):
    """Emite um certificado fictício de conclusão de trilha."""

    click.echo(f"\n  🎓 Gerando certificado para: {nome}")
    click.echo(f"  📚 Trilha: {tema}\n")

    certificado = generate_certificado(nome_participante=nome, tema=tema)

    if not certificado:
        temas_disponiveis = list_available_temas()
        click.echo(f"  ❌ Tema '{tema}' não encontrado.")
        click.echo(f"  Temas disponíveis: {', '.join(temas_disponiveis)}\n")
        return

    # Exibir certificado no terminal
    largura = 62
    linha = "═" * largura

    def centralizar(texto: str) -> str:
        return texto.center(largura)

    click.echo(f"  ╔{linha}╗")
    click.echo(f"  ║{centralizar('CERTIFICADO DE CONCLUSÃO')}║")
    click.echo(f"  ║{centralizar('Ethics Explorer')}║")
    click.echo(f"  ╠{linha}╣")
    click.echo(f"  ║{'':62}║")
    click.echo(f"  ║{centralizar('Certificamos que')}║")
    click.echo(f"  ║{'':62}║")
    click.echo(f"  ║{centralizar(certificado.nome_participante.upper())}║")
    click.echo(f"  ║{'':62}║")
    click.echo(f"  ║{centralizar('concluiu com êxito a trilha:')}║")
    click.echo(f"  ║{centralizar(certificado.titulo_trilha)}║")
    click.echo(f"  ║{'':62}║")
    click.echo(
        f"  ║{centralizar(f'Data: {certificado.data_emissao}  |  Código: {certificado.codigo_verificacao}')}║"
    )
    click.echo(f"  ║{'':62}║")
    click.echo(f"  ╚{linha}╝")

    click.echo()
    click.echo(f"  ✅ Certificado salvo em:")
    click.echo(f"  📁 {certificado.caminho_arquivo}\n")
