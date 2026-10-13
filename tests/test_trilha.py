"""
Testes do comando e serviço de trilhas.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.services import get_trilha, list_trilhas
from src.models import Trilha, Modulo


class TestGetTrilha:
    """Testes para src/services.py :: get_trilha()"""

    def test_retorna_trilha_valida_pelo_tema(self):
        trilha = get_trilha("lgpd")
        assert trilha is not None
        assert isinstance(trilha, Trilha)
        assert trilha.categoria == "lgpd"

    def test_retorna_none_para_tema_inexistente(self):
        trilha = get_trilha("tema_que_nao_existe")
        assert trilha is None

    def test_trilha_possui_modulos(self):
        trilha = get_trilha("lgpd")
        assert trilha is not None
        assert len(trilha.modulos) > 0
        assert all(isinstance(m, Modulo) for m in trilha.modulos)

    def test_modulos_possuem_topicos_e_recursos(self):
        trilha = get_trilha("compliance")
        assert trilha is not None
        for modulo in trilha.modulos:
            assert len(modulo.topicos) > 0
            assert len(modulo.recursos) > 0

    def test_normaliza_tema_case_insensitive(self):
        trilha_lower = get_trilha("lgpd")
        trilha_upper = get_trilha("LGPD")
        trilha_mixed = get_trilha("Lgpd")
        assert trilha_lower is not None
        assert trilha_upper is not None
        assert trilha_mixed is not None
        assert trilha_lower.titulo == trilha_upper.titulo == trilha_mixed.titulo

    def test_trilha_possui_duracao_estimada(self):
        trilha = get_trilha("etica_profissional")
        assert trilha is not None
        assert trilha.duracao_estimada != ""

    @pytest.mark.parametrize("tema", [
        "etica_profissional",
        "compliance",
        "lgpd",
        "seguranca_informacao",
        "conduta_organizacional",
        "combate_corrupcao",
    ])
    def test_todas_trilhas_existem(self, tema):
        trilha = get_trilha(tema)
        assert trilha is not None, f"Trilha '{tema}' não encontrada"
        assert trilha.titulo != ""
        assert trilha.descricao != ""


class TestListTrilhas:
    """Testes para src/services.py :: list_trilhas()"""

    def test_retorna_lista_nao_vazia(self):
        trilhas = list_trilhas()
        assert isinstance(trilhas, list)
        assert len(trilhas) > 0

    def test_retorna_objetos_trilha(self):
        trilhas = list_trilhas()
        assert all(isinstance(t, Trilha) for t in trilhas)

    def test_todas_trilhas_possuem_id_unico(self):
        trilhas = list_trilhas()
        ids = [t.id for t in trilhas]
        assert len(ids) == len(set(ids)), "Existem IDs duplicados nas trilhas"
