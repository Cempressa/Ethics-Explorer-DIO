"""
Ethics Explorer — Camada de serviços.

Contém a lógica de negócio reutilizável por comandos CLI e ferramentas MCP.
Esta é a camada que será adaptada para integração com Appwrite no futuro.
"""

import random
from typing import Optional

from src.models import Categoria, Certificado, Desafio, Modulo, Trilha
from src.utils import (
    ensure_certificates_dir,
    generate_verification_code,
    get_current_date,
    load_json,
    normalize_tema,
)


# ---------------------------------------------------------------------------
# Serviços de Trilha
# ---------------------------------------------------------------------------

def get_trilha(tema: str) -> Optional[Trilha]:
    """
    Busca e retorna uma trilha de estudos pelo tema.

    Args:
        tema: ID do tema (ex: 'lgpd', 'compliance').

    Returns:
        Objeto Trilha ou None se não encontrado.
    """
    tema_normalizado = normalize_tema(tema)
    data = load_json("trilhas.json")

    for item in data.get("trilhas", []):
        if item["categoria"] == tema_normalizado:
            modulos = [
                Modulo(
                    ordem=m["ordem"],
                    titulo=m["titulo"],
                    objetivo=m["objetivo"],
                    topicos=m.get("topicos", []),
                    recursos=m.get("recursos", []),
                )
                for m in item.get("modulos", [])
            ]
            return Trilha(
                id=item["id"],
                categoria=item["categoria"],
                titulo=item["titulo"],
                descricao=item["descricao"],
                duracao_estimada=item["duracao_estimada"],
                modulos=modulos,
            )
    return None


def list_trilhas() -> list[Trilha]:
    """
    Retorna todas as trilhas disponíveis.

    Returns:
        Lista de objetos Trilha.
    """
    data = load_json("trilhas.json")
    trilhas = []
    for item in data.get("trilhas", []):
        trilhas.append(
            Trilha(
                id=item["id"],
                categoria=item["categoria"],
                titulo=item["titulo"],
                descricao=item["descricao"],
                duracao_estimada=item["duracao_estimada"],
                modulos=[],
            )
        )
    return trilhas


# ---------------------------------------------------------------------------
# Serviços de Desafio
# ---------------------------------------------------------------------------

def get_desafios(tema: str, nivel: str) -> list[Desafio]:
    """
    Retorna todos os desafios de um tema e nível específicos.

    Args:
        tema: ID do tema.
        nivel: Nível de dificuldade ('iniciante', 'intermediario', 'avancado').

    Returns:
        Lista de objetos Desafio.
    """
    tema_normalizado = normalize_tema(tema)
    nivel_normalizado = nivel.lower().strip()
    data = load_json("desafios.json")

    desafios = []
    for item in data.get("desafios", []):
        if item["categoria"] == tema_normalizado and item["nivel"] == nivel_normalizado:
            desafios.append(
                Desafio(
                    id=item["id"],
                    categoria=item["categoria"],
                    nivel=item["nivel"],
                    pergunta=item["pergunta"],
                    alternativas=item["alternativas"],
                    resposta_correta=item["resposta_correta"],
                    explicacao=item["explicacao"],
                )
            )
    return desafios


def get_desafio_aleatorio(tema: Optional[str] = None, nivel: Optional[str] = None) -> Optional[Desafio]:
    """
    Retorna um desafio aleatório, com filtros opcionais de tema e nível.

    Args:
        tema: ID do tema (opcional).
        nivel: Nível de dificuldade (opcional).

    Returns:
        Objeto Desafio aleatório ou None se não houver desafios disponíveis.
    """
    data = load_json("desafios.json")
    candidatos = data.get("desafios", [])

    if tema:
        tema_normalizado = normalize_tema(tema)
        candidatos = [d for d in candidatos if d["categoria"] == tema_normalizado]

    if nivel:
        nivel_normalizado = nivel.lower().strip()
        candidatos = [d for d in candidatos if d["nivel"] == nivel_normalizado]

    if not candidatos:
        return None

    item = random.choice(candidatos)
    return Desafio(
        id=item["id"],
        categoria=item["categoria"],
        nivel=item["nivel"],
        pergunta=item["pergunta"],
        alternativas=item["alternativas"],
        resposta_correta=item["resposta_correta"],
        explicacao=item["explicacao"],
    )


# ---------------------------------------------------------------------------
# Serviços de Certificado
# ---------------------------------------------------------------------------

def generate_certificado(nome_participante: str, tema: str) -> Optional[Certificado]:
    """
    Gera um certificado fictício de conclusão de trilha e salva em arquivo.

    Args:
        nome_participante: Nome completo do participante.
        tema: ID do tema concluído.

    Returns:
        Objeto Certificado com caminho do arquivo salvo, ou None se o tema não existir.
    """
    trilha = get_trilha(tema)
    if not trilha:
        return None

    codigo = generate_verification_code()
    data_emissao = get_current_date()

    certificado = Certificado(
        nome_participante=nome_participante,
        titulo_trilha=trilha.titulo,
        categoria=trilha.categoria,
        data_emissao=data_emissao,
        codigo_verificacao=codigo,
    )

    # Salvar arquivo
    cert_dir = ensure_certificates_dir()
    nome_arquivo = f"certificado_{nome_participante.lower().replace(' ', '_')}_{trilha.categoria}.txt"
    caminho = cert_dir / nome_arquivo

    conteudo = _render_certificado_txt(certificado)
    caminho.write_text(conteudo, encoding="utf-8")
    certificado.caminho_arquivo = str(caminho)

    return certificado


def _render_certificado_txt(cert: Certificado) -> str:
    """
    Renderiza um certificado como texto formatado ASCII.

    Args:
        cert: Objeto Certificado.

    Returns:
        String formatada do certificado.
    """
    largura = 62
    linha = "═" * largura

    def centralizar(texto: str) -> str:
        return texto.center(largura)

    linhas = [
        f"╔{linha}╗",
        f"║{centralizar('CERTIFICADO DE CONCLUSÃO')}║",
        f"║{centralizar('Ethics Explorer')}║",
        f"╠{linha}╣",
        f"║{'':62}║",
        f"║{centralizar('Certificamos que')}║",
        f"║{'':62}║",
        f"║{centralizar(cert.nome_participante.upper())}║",
        f"║{'':62}║",
        f"║{centralizar('concluiu com êxito a trilha:')}║",
        f"║{centralizar(cert.titulo_trilha)}║",
        f"║{'':62}║",
        f"║{centralizar(f'Data: {cert.data_emissao}  |  Código: {cert.codigo_verificacao}')}║",
        f"║{'':62}║",
        f"╚{linha}╝",
    ]

    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Serviços de Categoria
# ---------------------------------------------------------------------------

def list_categorias() -> list[Categoria]:
    """
    Retorna todas as categorias disponíveis.

    Returns:
        Lista de objetos Categoria.
    """
    data = load_json("categorias.json")
    return [
        Categoria(
            id=cat["id"],
            nome=cat["nome"],
            descricao=cat["descricao"],
            nivel_minimo=cat["nivel_minimo"],
            icone=cat["icone"],
        )
        for cat in data.get("categorias", [])
    ]
