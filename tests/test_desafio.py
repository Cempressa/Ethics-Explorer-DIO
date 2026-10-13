"""
Testes do comando e serviço de desafios.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.services import get_desafios, get_desafio_aleatorio
from src.models import Desafio


class TestGetDesafios:
    """Testes para src/services.py :: get_desafios()"""

    def test_retorna_desafios_para_tema_e_nivel_validos(self):
        desafios = get_desafios("lgpd", "iniciante")
        assert isinstance(desafios, list)
        assert len(desafios) > 0

    def test_retorna_lista_vazia_para_nivel_inexistente(self):
        desafios = get_desafios("lgpd", "nivel_que_nao_existe")
        assert desafios == []

    def test_retorna_lista_vazia_para_tema_inexistente(self):
        desafios = get_desafios("tema_invalido", "iniciante")
        assert desafios == []

    def test_desafios_possuem_estrutura_correta(self):
        desafios = get_desafios("lgpd", "iniciante")
        for desafio in desafios:
            assert isinstance(desafio, Desafio)
            assert desafio.id != ""
            assert desafio.pergunta != ""
            assert len(desafio.alternativas) == 4
            assert desafio.resposta_correta in ("A", "B", "C", "D")
            assert desafio.explicacao != ""

    def test_desafios_filtrados_por_categoria(self):
        desafios = get_desafios("compliance", "intermediario")
        for desafio in desafios:
            assert desafio.categoria == "compliance"
            assert desafio.nivel == "intermediario"

    @pytest.mark.parametrize("tema,nivel", [
        ("etica_profissional", "iniciante"),
        ("compliance", "iniciante"),
        ("lgpd", "iniciante"),
        ("seguranca_informacao", "iniciante"),
        ("conduta_organizacional", "iniciante"),
        ("combate_corrupcao", "iniciante"),
    ])
    def test_todas_categorias_possuem_desafios_iniciante(self, tema, nivel):
        desafios = get_desafios(tema, nivel)
        assert len(desafios) > 0, f"Sem desafios para tema='{tema}' nivel='{nivel}'"


class TestGetDesafioAleatorio:
    """Testes para src/services.py :: get_desafio_aleatorio()"""

    def test_retorna_desafio_sem_filtros(self):
        desafio = get_desafio_aleatorio()
        assert desafio is not None
        assert isinstance(desafio, Desafio)

    def test_retorna_desafio_com_tema(self):
        desafio = get_desafio_aleatorio(tema="lgpd")
        assert desafio is not None
        assert desafio.categoria == "lgpd"

    def test_retorna_desafio_com_nivel(self):
        desafio = get_desafio_aleatorio(nivel="avancado")
        assert desafio is not None
        assert desafio.nivel == "avancado"

    def test_retorna_desafio_com_tema_e_nivel(self):
        desafio = get_desafio_aleatorio(tema="lgpd", nivel="intermediario")
        assert desafio is not None
        assert desafio.categoria == "lgpd"
        assert desafio.nivel == "intermediario"

    def test_retorna_none_para_filtro_sem_resultados(self):
        desafio = get_desafio_aleatorio(tema="tema_invalido", nivel="avancado")
        assert desafio is None

    def test_alternativas_tem_prefixo_correto(self):
        desafio = get_desafio_aleatorio()
        assert desafio is not None
        prefixos = ["A)", "B)", "C)", "D)"]
        for i, alt in enumerate(desafio.alternativas):
            assert alt.startswith(prefixos[i]), f"Alternativa {i} sem prefixo esperado"
