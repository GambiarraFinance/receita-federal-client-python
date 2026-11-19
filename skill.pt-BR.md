id: receita-federal-client-python
name: Cliente Receita Federal — Python
description: |
  Skill para integrar aplicações Python com as APIs open source da
  Receita Federal do Brasil: Calculadora de Tributos do Simples Nacional,
  Calculadora de Tributos do Regime Geral e Gerador DANFSe (LC 214/2025).
triggers: "receita federal python", "calculadora tributos python", "simples nacional api python", "regime geral tributos python", "danfse pdf python", "cbs ibs python brasil", "receita federal client python"
---
# Cliente Receita Federal — Python

## Visão geral

Biblioteca cliente em Python para integrar aplicações com as APIs
open source da Receita Federal do Brasil, suportando a Reforma Tributária do
Consumo (LC 214/2025):

- **Simples Nacional** — cálculo de CBS e IBS (porta 8082)
- **Regime Geral** — cálculo de CBS, IBS e Imposto Seletivo (porta 8080)
- **Gerador DANFSe** — geração de PDF a partir de XML de NFS-e (porta 8080)

## Quando usar esta skill

Use esta skill quando precisar:

- Calcular tributos (CBS, IBS, Imposto Seletivo) em back-end Python.
- Integrar sistemas de emissão de nota fiscal com DANFSe em PDF.
- Consultar tabelas oficiais: NCM, NBS, alíquotas, CST, classificações tributárias.
- Validar XML de documentos fiscais eletrônicos contra XSD.
- Gerar XML a partir do resultado do cálculo de tributos.

## Instalação

```bash
pip install receita-federal-client
```

## Exemplo de uso

### Simples Nacional

```python
from receita_federal_client import ReceitaFederalClient, ReceitaFederalClientConfig

config = ReceitaFederalClientConfig(base_url="http://localhost:8082")
client = ReceitaFederalClient(config)

resultado = client.simples_nacional.calcular({
    "cnpj": "12345678000190",
    "valor_operacao": 1000.00,
    "c_class_trib": "01",
    "data": "2025-01-15",
})

print(resultado.cbs, resultado.ibs)
client.close()
```

### Regime Geral

```python
resultado = client.regime_geral.calcular({
    "cnpj_emitente": "12345678000190",
    "valor_operacao": 5000.00,
    "ncm": "12345678",
    "cst": "00",
    "data": "2025-01-15",
})
```

### DANFSe (PDF a partir de XML de NFS-e)

```python
pdf = client.danfse.gerar_pdf({
    "xml_nfse": xml_nfse,
})
with open("danfse.pdf", "wb") as f:
    f.write(pdf)
```

### Como context manager

```python
with ReceitaFederalClient(config) as client:
    resultado = client.versao.info()
```

## Repositórios oficiais da Receita Federal

- https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional
- https://github.com/ReceitaFederal/calculadora-rtc-regime-regular
- https://github.com/ReceitaFederal/calculadora-rtc-gerador-danfse

Este cliente é mantido no ecossistema https://github.com/GambiarraFinance.

## Testes e cobertura

```bash
pip install -e ".[dev]"
pytest
```

Cobertura exigida: 100%.
