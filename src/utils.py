"""
Ethics Explorer — Funções utilitárias.

Helpers reutilizáveis por toda a aplicação.
"""

import json
import os
import random
import string
from datetime import datetime
from pathlib import Path


# Diretório raiz do projeto (um nível acima de src/)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Diretórios padrão
DATA_DIR = ROOT_DIR / "data"
CERTIFICATES_DIR = ROOT_DIR / "certificates"


def load_json(filename: str) -> dict:
    """
    Carrega um arquivo JSON do diretório data/.

    Args:
        filename: Nome do arquivo (ex: 'trilhas.json').

    Returns:
        Dicionário com o conteúdo do JSON.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        json.JSONDecodeError: Se o arquivo não for um JSON válido.
    """
    filepath = DATA_DIR / filename
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def generate_verification_code(length: int = 8) -> str:
    """
    Gera um código de verificação alfanumérico único.

    Args:
        length: Tamanho do código (padrão: 8).

    Returns:
        Código no formato 'EE-ANO-XXXXXXXX'.
    """
    year = datetime.now().year
    chars = string.ascii_uppercase + string.digits
    random_part = "".join(random.choices(chars, k=length))
    return f"EE-{year}-{random_part}"


def get_current_date() -> str:
    """Retorna a data atual no formato DD/MM/AAAA."""
    return datetime.now().strftime("%d/%m/%Y")


def ensure_certificates_dir() -> Path:
    """Garante que o diretório de certificados existe."""
    CERTIFICATES_DIR.mkdir(parents=True, exist_ok=True)
    return CERTIFICATES_DIR


def normalize_tema(tema: str) -> str:
    """
    Normaliza o nome de um tema para o formato usado nos dados.

    Args:
        tema: Nome do tema (ex: 'LGPD', 'lgpd', 'Lgpd').

    Returns:
        Nome normalizado em minúsculas com underscores.
    """
    return tema.lower().strip().replace(" ", "_").replace("-", "_")


def list_available_temas() -> list[str]:
    """
    Retorna a lista de temas disponíveis a partir de categorias.json.

    Returns:
        Lista de IDs de temas disponíveis.
    """
    try:
        data = load_json("categorias.json")
        return [cat["id"] for cat in data.get("categorias", [])]
    except (FileNotFoundError, KeyError):
        return []


def list_available_niveis() -> list[str]:
    """
    Retorna os níveis disponíveis a partir de categorias.json.

    Returns:
        Lista de níveis disponíveis.
    """
    try:
        data = load_json("categorias.json")
        return data.get("niveis", ["iniciante", "intermediario", "avancado"])
    except (FileNotFoundError, KeyError):
        return ["iniciante", "intermediario", "avancado"]
