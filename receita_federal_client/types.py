"""Tipos de dados do cliente Receita Federal."""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class ReceitaFederalClientConfig(BaseModel):
    """Configuração do cliente."""

    base_url: str
    timeout: int = 10000
    headers: dict = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Simples Nacional
# ---------------------------------------------------------------------------

class SimplesNacionalCalculoInput(BaseModel):
    cnpj: str
    valor_operacao: float = Field(..., gt=0)
    c_class_trib: str
    data: str

    @validator("data")
    def validar_data(cls, v: str) -> str:
        # Formato esperado: AAAA-MM-DD
        try:
            date.fromisoformat(v)
        except ValueError as exc:
            raise ValueError("data deve estar no formato AAAA-MM-DD") from exc
        return v


class SimplesNacionalItemErro(BaseModel):
    item: int
    codigo: str
    mensagem: str


class SimplesNacionalCalculoOutput(BaseModel):
    cbs: float
    ibs: float
    valor_total: float
    erros_por_item: List[SimplesNacionalItemErro] = Field(default_factory=list)
    sucesso: bool = True


class AtividadeSimples(BaseModel):
    codigo: str
    descricao: str
    anexo: str
    tipo_documento: str
    c_class_trib: str
    vigencia_inicio: str
    vigencia_fim: Optional[str] = None


class ErroVSN(BaseModel):
    codigo: str
    descricao: str


# ---------------------------------------------------------------------------
# Regime Geral
# ---------------------------------------------------------------------------

class RegimeGeralCalculoInput(BaseModel):
    cnpj_emitente: str
    valor_operacao: float = Field(..., gt=0)
    ncm: str
    cst: str
    data: str
    aliquota_ibs: Optional[float] = None
    aliquota_cbs: Optional[float] = None

    @validator("data")
    def validar_data(cls, v: str) -> str:
        try:
            date.fromisoformat(v)
        except ValueError as exc:
            raise ValueError("data deve estar no formato AAAA-MM-DD") from exc
        return v


class RegimeGeralItemErro(BaseModel):
    item: int
    codigo: str
    mensagem: str


class RegimeGeralCalculoOutput(BaseModel):
    cbs: float
    ibs: float
    imposto_seletivo: float
    valor_total: float
    erros_por_item: List[RegimeGeralItemErro] = Field(default_factory=list)
    sucesso: bool = True


class ErroREG(BaseModel):
    codigo: str
    descricao: str


class BaseCalculoUnificadaInput(BaseModel):
    cnpj: str
    valor_operacao: float = Field(..., gt=0)
    ncm: str
    tipo_documento: str  # 'nfe', 'nfce', 'nfse'


class BaseCalculoUnificadaOutput(BaseModel):
    base_calculo: float
    aliquota_aplicada: float
    valor_tributo: float


# ---------------------------------------------------------------------------
# DANFSe / XML
# ---------------------------------------------------------------------------

class DanfseGerarPDFInput(BaseModel):
    xml_nfse: str
    opcoes: Optional[dict] = None


class XmlGerarInput(BaseModel):
    tipo: str  # 'nfe', 'nfce', 'nfse'
    dados: dict


class XmlValidarInput(BaseModel):
    tipo: str  # 'nfe', 'nfce', 'nfse'
    subtipo: str  # 'grupo', 'nota'
    xml: str


class XmlValidarOutput(BaseModel):
    valido: bool
    erros: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Dados abertos
# ---------------------------------------------------------------------------

class SituacaoTributaria(BaseModel):
    codigo: str
    descricao: str
    regime: str  # 'cbs', 'ibs', 'ambos'


class ClassificacaoTributaria(BaseModel):
    codigo: str
    descricao: str


class FundamentoLegal(BaseModel):
    codigo: str
    descricao: str
    lei: str
    artigo: str


class AliquotaReferencia(BaseModel):
    uf: str
    municipio: str
    valor: float
    vigencia: str


class NCM(BaseModel):
    codigo: str
    descricao: str


class NBS(BaseModel):
    codigo: str
    descricao: str


# ---------------------------------------------------------------------------
# Versão
# ---------------------------------------------------------------------------

class VersaoInfo(BaseModel):
    aplicacao: str
    versao: str
    ambiente: str
    banco_dados: str


class VersaoStatus(BaseModel):
    perfil: str  # 'online', 'offline'
    sincronizado: bool
    diferenca: str
