"""Testes do cliente Receita Federal com 100% de cobertura."""

from unittest.mock import MagicMock

import httpx
import pytest
from pydantic import ValidationError

from receita_federal_client.client import (
    ReceitaFederalClient,
    SimplesNacionalApi,
    RegimeGeralApi,
    DanfseApi,
    VersaoApi,
)
from receita_federal_client.exceptions import ReceitaFederalError
from receita_federal_client.types import (
    SimplesNacionalCalculoInput,
    RegimeGeralCalculoInput,
    DanfseGerarPDFInput,
    ReceitaFederalClientConfig,
    BaseCalculoUnificadaInput,
)


class TestReceitaFederalError:
    def test_instanciar_com_mensagem_codigo_status(self):
        erro = ReceitaFederalError("Erro teste", "COD-001", 500)
        assert erro.message == "Erro teste"
        assert erro.codigo == "COD-001"
        assert erro.status_code == 500

    def test_instanciar_apenas_mensagem(self):
        erro = ReceitaFederalError("Erro simples")
        assert erro.message == "Erro simples"
        assert erro.codigo is None
        assert erro.status_code is None

    def test_eh_instancia_de_exception(self):
        erro = ReceitaFederalError("teste")
        assert isinstance(erro, Exception)

    def test_str_com_codigo(self):
        erro = ReceitaFederalError("Erro teste", "COD-001", 500)
        assert str(erro) == "[COD-001] Erro teste"

    def test_str_sem_codigo(self):
        erro = ReceitaFederalError("Erro simples")
        assert str(erro) == "Erro simples"

    def test_repr(self):
        erro = ReceitaFederalError("msg", "COD", 400)
        r = repr(erro)
        assert "ReceitaFederalError" in r
        assert "msg" in r
        assert "COD" in r


class TestSimplesNacionalApi:
    def setup_method(self):
        self.mock_http = MagicMock(spec=httpx.Client)
        self.api = SimplesNacionalApi(self.mock_http)

    def test_calcular_sucesso(self):
        input_data = SimplesNacionalCalculoInput(
            cnpj="12345678000190",
            valor_operacao=1000.00,
            c_class_trib="01",
            data="2025-01-15",
        )
        self.mock_http.post.return_value.json.return_value = {
            "cbs": 100,
            "ibs": 50,
            "valor_total": 150,
            "erros_por_item": [],
            "sucesso": True,
        }
        self.mock_http.post.return_value.status_code = 200

        resultado = self.api.calcular(input_data)

        assert resultado.cbs == 100
        assert resultado.ibs == 50
        assert resultado.sucesso is True
        self.mock_http.post.assert_called_once_with(
            "/calculadora/observabilidade/simples-nacional",
            json=input_data.dict(),
        )

    def test_calcular_erro_http(self):
        input_data = SimplesNacionalCalculoInput(
            cnpj="12345678000190",
            valor_operacao=1000.00,
            c_class_trib="01",
            data="2025-01-15",
        )
        response = MagicMock(spec=httpx.Response)
        response.status_code = 500
        response.text = "Internal Server Error"
        self.mock_http.post.return_value = response

        with pytest.raises(ReceitaFederalError) as exc:
            self.api.calcular(input_data)
        assert exc.value.status_code == 500

    def test_atividades_sem_data(self):
        self.mock_http.get.return_value.json.return_value = []
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.atividades()

        assert resultado == []
        self.mock_http.get.assert_called_once_with(
            "/calculadora/simples-nacional/atividades", params={}
        )

    def test_atividades_com_data(self):
        self.mock_http.get.return_value.json.return_value = []
        self.mock_http.get.return_value.status_code = 200

        self.api.atividades(data="2025-01-15")

        self.mock_http.get.assert_called_once_with(
            "/calculadora/simples-nacional/atividades",
            params={"data": "2025-01-15"},
        )

    def test_atividade_por_codigo_sucesso(self):
        self.mock_http.get.return_value.json.return_value = {
            "codigo": "01",
            "descricao": "Atividade",
            "anexo": "I",
            "tipo_documento": "NF-e",
            "c_class_trib": "01",
            "vigencia_inicio": "2025-01-01",
        }
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.atividade_por_codigo("01")

        assert resultado.codigo == "01"
        self.mock_http.get.assert_called_once_with(
            "/calculadora/simples-nacional/atividades/01", params={}
        )

    def test_atividade_por_codigo_com_data(self):
        self.mock_http.get.return_value.json.return_value = {
            "codigo": "01",
            "descricao": "Atividade",
            "anexo": "I",
            "tipo_documento": "NF-e",
            "c_class_trib": "01",
            "vigencia_inicio": "2025-01-01",
        }
        self.mock_http.get.return_value.status_code = 200

        self.api.atividade_por_codigo("01", data="2025-01-15")

        self.mock_http.get.assert_called_once_with(
            "/calculadora/simples-nacional/atividades/01",
            params={"data": "2025-01-15"},
        )

    def test_descricao_erro_sucesso(self):
        self.mock_http.get.return_value.json.return_value = {
            "codigo": "VSN-001",
            "descricao": "Erro de exemplo",
        }
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.descricao_erro("VSN-001")

        assert resultado.codigo == "VSN-001"
        self.mock_http.get.assert_called_once_with(
            "/calculadora/observabilidade/simples-nacional/erros",
            params={"codigo": "VSN-001"},
        )


class TestRegimeGeralApi:
    def setup_method(self):
        self.mock_http = MagicMock(spec=httpx.Client)
        self.api = RegimeGeralApi(self.mock_http)

    def _input_valido(self):
        return RegimeGeralCalculoInput(
            cnpj_emitente="12345678000190",
            valor_operacao=5000.00,
            ncm="12345678",
            cst="00",
            data="2025-01-15",
        )

    def test_calcular_sucesso(self):
        input_data = self._input_valido()
        self.mock_http.post.return_value.json.return_value = {
            "cbs": 200,
            "ibs": 100,
            "imposto_seletivo": 50,
            "valor_total": 350,
            "erros_por_item": [],
            "sucesso": True,
        }
        self.mock_http.post.return_value.status_code = 200

        resultado = self.api.calcular(input_data)

        assert resultado.cbs == 200
        assert resultado.imposto_seletivo == 50
        self.mock_http.post.assert_called_once_with(
            "/regime-geral", json=input_data.dict()
        )

    def test_calcular_erro_http(self):
        input_data = self._input_valido()
        response = MagicMock(spec=httpx.Response)
        response.status_code = 500
        response.text = "Internal Server Error"
        self.mock_http.post.return_value = response

        with pytest.raises(ReceitaFederalError) as exc:
            self.api.calcular(input_data)
        assert exc.value.status_code == 500

    def test_calcular_observavel_sucesso(self):
        input_data = self._input_valido()
        self.mock_http.post.return_value.json.return_value = {
            "cbs": 200,
            "ibs": 100,
            "imposto_seletivo": 50,
            "valor_total": 350,
            "erros_por_item": [],
            "sucesso": True,
        }
        self.mock_http.post.return_value.status_code = 200

        resultado = self.api.calcular_observavel(input_data)

        assert resultado.sucesso is True
        self.mock_http.post.assert_called_once_with(
            "/observabilidade/regime-geral", json=input_data.dict()
        )

    def test_descricao_erro_sucesso(self):
        self.mock_http.get.return_value.json.return_value = {
            "codigo": "REG-011",
            "descricao": "Erro de exemplo",
        }
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.descricao_erro("REG-011")

        assert resultado.codigo == "REG-011"
        self.mock_http.get.assert_called_once_with(
            "/observabilidade/erros", params={"codigo": "REG-011"}
        )

    def test_base_calculo_unificada_sucesso(self):
        input_data = BaseCalculoUnificadaInput(
            cnpj="12345678000190",
            valor_operacao=1000,
            ncm="12345678",
            tipo_documento="nfe",
        )
        self.mock_http.post.return_value.json.return_value = {
            "base_calculo": 1000,
            "aliquota_aplicada": 0.1,
            "valor_tributo": 100,
        }
        self.mock_http.post.return_value.status_code = 200

        resultado = self.api.base_calculo_unificada(input_data)

        assert resultado.base_calculo == 1000
        self.mock_http.post.assert_called_once_with(
            "/base-calculo/base-calculo-unificada",
            json=input_data.dict(),
        )

    def test_base_calculo_unificada_nfse_sucesso(self):
        input_data = BaseCalculoUnificadaInput(
            cnpj="12345678000190",
            valor_operacao=1000,
            ncm="12345678",
            tipo_documento="nfse",
        )
        self.mock_http.post.return_value.json.return_value = {
            "base_calculo": 1000,
            "aliquota_aplicada": 0.1,
            "valor_tributo": 100,
        }
        self.mock_http.post.return_value.status_code = 200

        resultado = self.api.base_calculo_unificada_nfse(input_data)

        assert resultado.valor_tributo == 100
        self.mock_http.post.assert_called_once_with(
            "/base-calculo/base-calculo-unificada-nfse",
            json=input_data.dict(),
        )

    def test_gerar_xml_sucesso(self):
        self.mock_http.post.return_value.text = "<xml></xml>"
        self.mock_http.post.return_value.status_code = 200

        resultado = self.api.gerar_xml("nfe", {})

        assert resultado == "<xml></xml>"

    def test_validar_xml_sucesso(self):
        self.mock_http.post.return_value.json.return_value = {
            "valido": True,
            "erros": [],
        }
        self.mock_http.post.return_value.status_code = 200

        resultado = self.api.validar_xml("nfe", "grupo", "<xml></xml>")

        assert resultado.valido is True

    def test_situacoes_tributarias_sucesso(self):
        self.mock_http.get.return_value.json.return_value = [
            {"codigo": "00", "descricao": "Tributada", "regime": "ambos"}
        ]
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.situacoes_tributarias()

        assert resultado[0].codigo == "00"

    def test_classificacoes_tributarias_sucesso(self):
        self.mock_http.get.return_value.json.return_value = [
            {"codigo": "1", "descricao": "Classificacao"}
        ]
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.classificacoes_tributarias()

        assert resultado[0].codigo == "1"

    def test_fundamentacoes_legais_sucesso(self):
        self.mock_http.get.return_value.json.return_value = [
            {
                "codigo": "LC214",
                "descricao": "Reforma Tributaria",
                "lei": "LC 214/2025",
                "artigo": "1",
            }
        ]
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.fundamentacoes_legais()

        assert resultado[0].lei == "LC 214/2025"

    def test_ncm_sucesso(self):
        self.mock_http.get.return_value.json.return_value = [
            {"codigo": "12345678", "descricao": "Produto"}
        ]
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.ncm()

        assert resultado[0].codigo == "12345678"

    def test_nbs_sucesso(self):
        self.mock_http.get.return_value.json.return_value = [
            {"codigo": "1234", "descricao": "Servico"}
        ]
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.nbs()

        assert resultado[0].codigo == "1234"

    def test_aliquota_uniao_sucesso(self):
        self.mock_http.get.return_value.json.return_value = [
            {"uf": "SP", "municipio": "", "valor": 0.1, "vigencia": "2025-01-01"}
        ]
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.aliquota_uniao()

        assert resultado[0].valor == 0.1

    def test_aliquota_uf_sucesso(self):
        self.mock_http.get.return_value.json.return_value = [
            {"uf": "SP", "municipio": "", "valor": 0.02, "vigencia": "2025-01-01"}
        ]
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.aliquota_uf("SP")

        assert resultado[0].uf == "SP"
        self.mock_http.get.assert_called_once_with("/dados-abertos/aliquota-uf/SP")

    def test_aliquota_municipio_sucesso(self):
        self.mock_http.get.return_value.json.return_value = [
            {
                "uf": "SP",
                "municipio": "Sao Paulo",
                "valor": 0.03,
                "vigencia": "2025-01-01",
            }
        ]
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.aliquota_municipio("Sao Paulo")

        assert resultado[0].municipio == "Sao Paulo"
        self.mock_http.get.assert_called_once_with(
            "/dados-abertos/aliquota-municipio/Sao Paulo"
        )


class TestDanfseApi:
    def setup_method(self):
        self.mock_http = MagicMock(spec=httpx.Client)
        self.api = DanfseApi(self.mock_http)

    def test_gerar_pdf_sucesso(self):
        input_data = DanfseGerarPDFInput(
            xml_nfse="<nfse></nfse>",
            opcoes={"modo_paisagem": False, "versao": "1.0"},
        )
        self.mock_http.post.return_value.content = b"pdf-conteudo"
        self.mock_http.post.return_value.status_code = 200

        resultado = self.api.gerar_pdf(input_data)

        assert resultado == b"pdf-conteudo"

    def test_gerar_pdf_erro_http(self):
        input_data = DanfseGerarPDFInput(xml_nfse="<nfse></nfse>")
        response = MagicMock(spec=httpx.Response)
        response.status_code = 500
        response.text = "Internal Server Error"
        self.mock_http.post.return_value = response

        with pytest.raises(ReceitaFederalError) as exc:
            self.api.gerar_pdf(input_data)
        assert exc.value.status_code == 500


class TestVersaoApi:
    def setup_method(self):
        self.mock_http = MagicMock(spec=httpx.Client)
        self.api = VersaoApi(self.mock_http)

    def test_info_sucesso(self):
        self.mock_http.get.return_value.json.return_value = {
            "aplicacao": "simples",
            "versao": "1.0",
            "ambiente": "producao",
            "banco_dados": "postgres",
        }
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.info()

        assert resultado.aplicacao == "simples"

    def test_info_erro_http(self):
        response = MagicMock(spec=httpx.Response)
        response.status_code = 500
        response.text = "Internal Server Error"
        self.mock_http.get.return_value = response

        with pytest.raises(ReceitaFederalError) as exc:
            self.api.info()
        assert exc.value.status_code == 500

    def test_status_sucesso(self):
        self.mock_http.get.return_value.json.return_value = {
            "perfil": "online",
            "sincronizado": True,
            "diferenca": "0s",
        }
        self.mock_http.get.return_value.status_code = 200

        resultado = self.api.status()

        assert resultado.perfil == "online"


class TestReceitaFederalClient:
    def test_instanciar_config_padrao(self):
        config = ReceitaFederalClientConfig(base_url="http://localhost:8082")
        client = ReceitaFederalClient(config)

        assert client.simples_nacional is not None
        assert client.regime_geral is not None
        assert client.danfse is not None
        assert client.versao is not None
        client.close()

    def test_instanciar_timeout_customizado(self):
        config = ReceitaFederalClientConfig(
            base_url="http://localhost:8082", timeout=5000
        )
        client = ReceitaFederalClient(config)
        assert client._http.timeout.connect == 5000
        client.close()

    def test_instanciar_headers_customizados(self):
        config = ReceitaFederalClientConfig(
            base_url="http://localhost:8082",
            headers={"X-Custom": "valor"},
        )
        client = ReceitaFederalClient(config)
        assert client._http.headers["X-Custom"] == "valor"
        client.close()

    def test_context_manager(self):
        config = ReceitaFederalClientConfig(base_url="http://localhost:8082")
        with ReceitaFederalClient(config) as client:
            assert client is not None

    def test_close(self):
        config = ReceitaFederalClientConfig(base_url="http://localhost:8082")
        client = ReceitaFederalClient(config)
        client._http.close = MagicMock()
        client.close()
        client._http.close.assert_called_once()


class TestTypesValidadores:
    def test_simples_nacional_data_invalida(self):
        with pytest.raises(ValidationError):
            SimplesNacionalCalculoInput(
                cnpj="12345678000190",
                valor_operacao=1000.00,
                c_class_trib="01",
                data="data-invalida",
            )

    def test_regime_geral_data_invalida(self):
        with pytest.raises(ValidationError):
            RegimeGeralCalculoInput(
                cnpj_emitente="12345678000190",
                valor_operacao=5000.00,
                ncm="12345678",
                cst="00",
                data="data-invalida",
            )

    def test_simples_nacional_valor_operacao_negativo(self):
        with pytest.raises(ValidationError):
            SimplesNacionalCalculoInput(
                cnpj="12345678000190",
                valor_operacao=-1.00,
                c_class_trib="01",
                data="2025-01-15",
            )
