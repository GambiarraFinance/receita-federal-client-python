"""Cliente Receita Federal — Python.

Integração com as APIs open source da Receita Federal do Brasil:
Simples Nacional, Regime Geral e Gerador DANFSe (LC 214/2025).
"""

from .client import ReceitaFederalClient
from .types import (
    SimplesNacionalCalculoInput,
    SimplesNacionalCalculoOutput,
    AtividadeSimples,
    ErroVSN,
    RegimeGeralCalculoInput,
    RegimeGeralCalculoOutput,
    ErroREG,
    BaseCalculoUnificadaInput,
    BaseCalculoUnificadaOutput,
    DanfseGerarPDFInput,
    XmlGerarInput,
    XmlValidarInput,
    XmlValidarOutput,
    SituacaoTributaria,
    ClassificacaoTributaria,
    FundamentoLegal,
    AliquotaReferencia,
    NCM,
    NBS,
    VersaoInfo,
    VersaoStatus,
)
from .exceptions import ReceitaFederalError

__version__ = "1.0.0"

__all__ = [
    "ReceitaFederalClient",
    "SimplesNacionalCalculoInput",
    "SimplesNacionalCalculoOutput",
    "AtividadeSimples",
    "ErroVSN",
    "RegimeGeralCalculoInput",
    "RegimeGeralCalculoOutput",
    "ErroREG",
    "BaseCalculoUnificadaInput",
    "BaseCalculoUnificadaOutput",
    "DanfseGerarPDFInput",
    "XmlGerarInput",
    "XmlValidarInput",
    "XmlValidarOutput",
    "SituacaoTributaria",
    "ClassificacaoTributaria",
    "FundamentoLegal",
    "AliquotaReferencia",
    "NCM",
    "NBS",
    "VersaoInfo",
    "VersaoStatus",
    "ReceitaFederalError",
]
