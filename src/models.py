"""
Ethics Explorer — Modelos de dados.

Define as estruturas de dados usadas em toda a aplicação
usando dataclasses padrão do Python.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Recurso:
    """Recurso de aprendizagem de um módulo."""
    descricao: str


@dataclass
class Modulo:
    """Módulo de uma trilha de estudos."""
    ordem: int
    titulo: str
    objetivo: str
    topicos: list[str] = field(default_factory=list)
    recursos: list[str] = field(default_factory=list)


@dataclass
class Trilha:
    """Trilha de estudos completa."""
    id: str
    categoria: str
    titulo: str
    descricao: str
    duracao_estimada: str
    modulos: list[Modulo] = field(default_factory=list)


@dataclass
class Categoria:
    """Categoria temática da plataforma."""
    id: str
    nome: str
    descricao: str
    nivel_minimo: str
    icone: str


@dataclass
class Desafio:
    """Desafio de conhecimento com múltipla escolha."""
    id: str
    categoria: str
    nivel: str
    pergunta: str
    alternativas: list[str]
    resposta_correta: str
    explicacao: str


@dataclass
class Certificado:
    """Certificado fictício de conclusão de trilha."""
    nome_participante: str
    titulo_trilha: str
    categoria: str
    data_emissao: str
    codigo_verificacao: str
    caminho_arquivo: Optional[str] = None
