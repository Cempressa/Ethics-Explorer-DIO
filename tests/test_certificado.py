"""
Testes do comando e serviço de certificados.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.services import generate_certificado
from src.models import Certificado
from src.utils import generate_verification_code, get_current_date


class TestGenerateCertificado:
    """Testes para src/services.py :: generate_certificado()"""

    def test_gera_certificado_valido(self, tmp_path, monkeypatch):
        """Gera certificado e verifica campos obrigatórios."""
        monkeypatch.setattr("src.utils.CERTIFICATES_DIR", tmp_path)
        monkeypatch.setattr("src.services.ensure_certificates_dir", lambda: tmp_path)

        certificado = generate_certificado("Maria Silva", "lgpd")

        assert certificado is not None
        assert isinstance(certificado, Certificado)
        assert certificado.nome_participante == "Maria Silva"
        assert "LGPD" in certificado.titulo_trilha
        assert certificado.categoria == "lgpd"
        assert certificado.data_emissao != ""
        assert certificado.codigo_verificacao.startswith("EE-")

    def test_retorna_none_para_tema_inexistente(self):
        certificado = generate_certificado("João Silva", "tema_invalido")
        assert certificado is None

    def test_codigo_verificacao_formato_correto(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.services.ensure_certificates_dir", lambda: tmp_path)

        certificado = generate_certificado("Ana Costa", "compliance")
        assert certificado is not None

        partes = certificado.codigo_verificacao.split("-")
        assert partes[0] == "EE"
        assert partes[1].isdigit()          # Ano
        assert len(partes[2]) == 8          # Código alfanumérico

    def test_arquivo_salvo_no_diretorio(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.services.ensure_certificates_dir", lambda: tmp_path)

        certificado = generate_certificado("Pedro Lima", "lgpd")
        assert certificado is not None
        assert certificado.caminho_arquivo is not None
        assert Path(certificado.caminho_arquivo).exists()

    def test_arquivo_contem_nome_participante(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.services.ensure_certificates_dir", lambda: tmp_path)

        certificado = generate_certificado("Carlos Mendes", "etica_profissional")
        assert certificado is not None

        conteudo = Path(certificado.caminho_arquivo).read_text(encoding="utf-8")
        assert "CARLOS MENDES" in conteudo

    def test_arquivo_contem_codigo_verificacao(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.services.ensure_certificates_dir", lambda: tmp_path)

        certificado = generate_certificado("Lucia Ferreira", "compliance")
        assert certificado is not None

        conteudo = Path(certificado.caminho_arquivo).read_text(encoding="utf-8")
        assert certificado.codigo_verificacao in conteudo

    @pytest.mark.parametrize("tema", [
        "etica_profissional",
        "compliance",
        "lgpd",
        "seguranca_informacao",
        "conduta_organizacional",
        "combate_corrupcao",
    ])
    def test_gera_certificado_para_todos_os_temas(self, tema, tmp_path, monkeypatch):
        monkeypatch.setattr("src.services.ensure_certificates_dir", lambda: tmp_path)

        certificado = generate_certificado("Teste Participante", tema)
        assert certificado is not None, f"Certificado não gerado para tema '{tema}'"


class TestUtils:
    """Testes para funções utilitárias em src/utils.py"""

    def test_generate_verification_code_formato(self):
        codigo = generate_verification_code()
        assert codigo.startswith("EE-")
        partes = codigo.split("-")
        assert len(partes) == 3
        assert len(partes[2]) == 8

    def test_generate_verification_code_unico(self):
        codigos = {generate_verification_code() for _ in range(100)}
        # Com alta probabilidade, 100 códigos aleatórios devem ser únicos
        assert len(codigos) > 90

    def test_get_current_date_formato(self):
        data = get_current_date()
        partes = data.split("/")
        assert len(partes) == 3
        assert len(partes[0]) == 2  # DD
        assert len(partes[1]) == 2  # MM
        assert len(partes[2]) == 4  # AAAA
