"""Cliente principal para as APIs da Receita Federal do Brasil."""

from typing import Any, Dict, List, Optional

import httpx

from .exceptions import ReceitaFederalError
from .types import (
    AliquotaReferencia,
    AtividadeSimples,
    BaseCalculoUnificadaInput,
    BaseCalculoUnificadaOutput,
    ClassificacaoTributaria,
    DanfseGerarPDFInput,
    ErroREG,
    ErroVSN,
    FundamentoLegal,
    NCM,
    NBS,
    RegimeGeralCalculoInput,
    RegimeGeralCalculoOutput,
    ReceitaFederalClientConfig,
    SituacaoTributaria,
    SimplesNacionalCalculoInput,
    SimplesNacionalCalculoOutput,
    VersaoInfo,
    VersaoStatus,
    XmlValidarInput,
    XmlValidarOutput,
)


class SimplesNacionalApi:
    """API do Simples Nacional."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def calcular(
        self, input_data: SimplesNacionalCalculoInput
    ) -> SimplesNacionalCalculoOutput:
        response = self._http.post(
            "/calculadora/observabilidade/simples-nacional",
            json=input_data.dict(),
        )
        self._tratar_erro(response)
        return SimplesNacionalCalculoOutput(**response.json())

    def atividades(self, data: Optional[str] = None) -> List[AtividadeSimples]:
        params: Dict[str, Any] = {}
        if data:
            params["data"] = data
        response = self._http.get(
            "/calculadora/simples-nacional/atividades", params=params
        )
        self._tratar_erro(response)
        return [AtividadeSimples(**item) for item in response.json()]

    def atividade_por_codigo(
        self, codigo: str, data: Optional[str] = None
    ) -> AtividadeSimples:
        params: Dict[str, Any] = {}
        if data:
            params["data"] = data
        response = self._http.get(
            f"/calculadora/simples-nacional/atividades/{codigo}", params=params
        )
        self._tratar_erro(response)
        return AtividadeSimples(**response.json())

    def descricao_erro(self, codigo: str) -> ErroVSN:
        response = self._http.get(
            "/calculadora/observabilidade/simples-nacional/erros",
            params={"codigo": codigo},
        )
        self._tratar_erro(response)
        return ErroVSN(**response.json())

    @staticmethod
    def _tratar_erro(response: httpx.Response) -> None:
        if response.status_code >= 400:
            raise ReceitaFederalError(
                message=response.text,
                status_code=response.status_code,
            )


class RegimeGeralApi:
    """API do Regime Geral."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def calcular(
        self, input_data: RegimeGeralCalculoInput
    ) -> RegimeGeralCalculoOutput:
        response = self._http.post("/regime-geral", json=input_data.dict())
        self._tratar_erro(response)
        return RegimeGeralCalculoOutput(**response.json())

    def calcular_observavel(
        self, input_data: RegimeGeralCalculoInput
    ) -> RegimeGeralCalculoOutput:
        response = self._http.post(
            "/observabilidade/regime-geral", json=input_data.dict()
        )
        self._tratar_erro(response)
        return RegimeGeralCalculoOutput(**response.json())

    def descricao_erro(self, codigo: str) -> ErroREG:
        response = self._http.get(
            "/observabilidade/erros", params={"codigo": codigo}
        )
        self._tratar_erro(response)
        return ErroREG(**response.json())

    def base_calculo_unificada(
        self, input_data: BaseCalculoUnificadaInput
    ) -> BaseCalculoUnificadaOutput:
        response = self._http.post(
            "/base-calculo/base-calculo-unificada", json=input_data.dict()
        )
        self._tratar_erro(response)
        return BaseCalculoUnificadaOutput(**response.json())

    def base_calculo_unificada_nfse(
        self, input_data: BaseCalculoUnificadaInput
    ) -> BaseCalculoUnificadaOutput:
        response = self._http.post(
            "/base-calculo/base-calculo-unificada-nfse", json=input_data.dict()
        )
        self._tratar_erro(response)
        return BaseCalculoUnificadaOutput(**response.json())

    def gerar_xml(self, tipo: str, dados: dict) -> str:
        response = self._http.post(
            "/xml/generate",
            json={"tipo": tipo, "dados": dados},
            params={"tipo": tipo},
        )
        self._tratar_erro(response)
        return response.text

    def validar_xml(
        self, tipo: str, subtipo: str, xml: str
    ) -> XmlValidarOutput:
        response = self._http.post(
            "/xml/validate",
            json={"tipo": tipo, "subtipo": subtipo, "xml": xml},
            params={"tipo": tipo, "subtipo": subtipo},
        )
        self._tratar_erro(response)
        return XmlValidarOutput(**response.json())

    def situacoes_tributarias(self) -> List[SituacaoTributaria]:
        response = self._http.get(
            "/dados-abertos/situacoes-tributarias/cbs-ibs"
        )
        self._tratar_erro(response)
        return [SituacaoTributaria(**item) for item in response.json()]

    def classificacoes_tributarias(self) -> List[ClassificacaoTributaria]:
        response = self._http.get(
            "/dados-abertos/classificacoes-tributarias"
        )
        self._tratar_erro(response)
        return [ClassificacaoTributaria(**item) for item in response.json()]

    def fundamentacoes_legais(self) -> List[FundamentoLegal]:
        response = self._http.get("/dados-abertos/fundamentacoes-legais")
        self._tratar_erro(response)
        return [FundamentoLegal(**item) for item in response.json()]

    def ncm(self) -> List[NCM]:
        response = self._http.get("/dados-abertos/ncm")
        self._tratar_erro(response)
        return [NCM(**item) for item in response.json()]

    def nbs(self) -> List[NBS]:
        response = self._http.get("/dados-abertos/nbs")
        self._tratar_erro(response)
        return [NBS(**item) for item in response.json()]

    def aliquota_uniao(self) -> List[AliquotaReferencia]:
        response = self._http.get("/dados-abertos/aliquota-uniao")
        self._tratar_erro(response)
        return [AliquotaReferencia(**item) for item in response.json()]

    def aliquota_uf(self, uf: str) -> List[AliquotaReferencia]:
        response = self._http.get(f"/dados-abertos/aliquota-uf/{uf}")
        self._tratar_erro(response)
        return [AliquotaReferencia(**item) for item in response.json()]

    def aliquota_municipio(self, municipio: str) -> List[AliquotaReferencia]:
        response = self._http.get(f"/dados-abertos/aliquota-municipio/{municipio}")
        self._tratar_erro(response)
        return [AliquotaReferencia(**item) for item in response.json()]

    @staticmethod
    def _tratar_erro(response: httpx.Response) -> None:
        if response.status_code >= 400:
            raise ReceitaFederalError(
                message=response.text,
                status_code=response.status_code,
            )


class DanfseApi:
    """API do Gerador DANFSe."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def gerar_pdf(self, input_data: DanfseGerarPDFInput) -> bytes:
        response = self._http.post(
            "/danfse/gerar-pdf",
            json=input_data.dict(),
        )
        self._tratar_erro(response)
        return response.content

    @staticmethod
    def _tratar_erro(response: httpx.Response) -> None:
        if response.status_code >= 400:
            raise ReceitaFederalError(
                message=response.text,
                status_code=response.status_code,
            )


class VersaoApi:
    """API de Versão e Status."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def info(self) -> VersaoInfo:
        response = self._http.get("/versao")
        self._tratar_erro(response)
        return VersaoInfo(**response.json())

    def status(self) -> VersaoStatus:
        response = self._http.get("/versao/status")
        self._tratar_erro(response)
        return VersaoStatus(**response.json())

    @staticmethod
    def _tratar_erro(response: httpx.Response) -> None:
        if response.status_code >= 400:
            raise ReceitaFederalError(
                message=response.text,
                status_code=response.status_code,
            )


class ReceitaFederalClient:
    """Cliente principal para integração com as APIs da Receita Federal.

    Suporta:
    - Simples Nacional (CBS, IBS) — porta 8082
    - Regime Geral (CBS, IBS, Imposto Seletivo) — porta 8080
    - Gerador DANFSe (PDF a partir de XML de NFS-e) — porta 8080
    """

    def __init__(self, config: ReceitaFederalClientConfig) -> None:
        self._http = httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            headers={
                "Content-Type": "application/json",
                **config.headers,
            },
        )
        self.simples_nacional = SimplesNacionalApi(self._http)
        self.regime_geral = RegimeGeralApi(self._http)
        self.danfse = DanfseApi(self._http)
        self.versao = VersaoApi(self._http)

    def close(self) -> None:
        """Fecha o cliente HTTP."""
        self._http.close()

    def __enter__(self) -> "ReceitaFederalClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
