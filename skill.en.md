id: receita-federal-client-python
name: Brazilian Federal Revenue Client — Python
description: |
  Skill to integrate Python applications with the open source APIs
  of the Brazilian Federal Revenue (Receita Federal do Brasil): Simple National
  Tax Calculator, General Regime Tax Calculator and DANFSe Generator (LC 214/2025).
triggers: "brazilian federal revenue python", "tax calculator python", "simple national api python", "general regime taxes python", "danfse pdf python", "cbs ibs python brazil", "receita federal client python"
---
# Brazilian Federal Revenue Client — Python

## Overview

Python client library to integrate applications with the open
source APIs of the Brazilian Federal Revenue (Receita Federal do Brasil),
supporting the Consumption Tax Reform (LC 214/2025):

- **Simple National** — CBS and IBS calculation (port 8082)
- **General Regime** — CBS, IBS and Selective Tax calculation (port 8080)
- **DANFSe Generator** — PDF generation from NFS-e XML (port 8080)

## When to use this skill

Use this skill when you need to:

- Calculate taxes (CBS, IBS, Selective Tax) in Python back-end.
- Integrate electronic invoicing systems with DANFSe PDF generation.
- Look up official tables: NCM, NBS, rates, CST, tax classifications.
- Validate electronic fiscal document XML against XSD.
- Generate XML from tax calculation results.

## Installation

```bash
pip install receita-federal-client
```

## Usage example

### Simple National

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

### General Regime

```python
resultado = client.regime_geral.calcular({
    "cnpj_emitente": "12345678000190",
    "valor_operacao": 5000.00,
    "ncm": "12345678",
    "cst": "00",
    "data": "2025-01-15",
})
```

### DANFSe (PDF from NFS-e XML)

```python
pdf = client.danfse.gerar_pdf({
    "xml_nfse": xml_nfse,
})
with open("danfse.pdf", "wb") as f:
    f.write(pdf)
```

### As context manager

```python
with ReceitaFederalClient(config) as client:
    resultado = client.versao.info()
```

## Official Receita Federal repositories

- https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional
- https://github.com/ReceitaFederal/calculadora-rtc-regime-regular
- https://github.com/ReceitaFederal/calculadora-rtc-gerador-danfse

This client is maintained in the https://github.com/GambiarraFinance ecosystem.

## Tests and coverage

```bash
pip install -e ".[dev]"
pytest
```

Coverage required: 100%.
