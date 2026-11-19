# receita-federal-client

Cliente Python para integração com as APIs open source da Receita
Federal do Brasil (Simples Nacional, Regime Geral e Gerador DANFSe — LC 214/2025).

## Principais recursos

- ✅ Cálculo de tributos no Simples Nacional (CBS e IBS)
- ✅ Cálculo de tributos no Regime Geral (CBS, IBS e Imposto Seletivo)
- ✅ Observabilidade por item (erros não interrompem os demais)
- ✅ Consulta de atividades do Simples Nacional vigentes em uma data
- ✅ Geração de DANFSe em PDF a partir de XML de NFS-e
- ✅ Geração e validação de XML de documentos fiscais eletrônicos
- ✅ Consulta de tabelas oficiais: NCM, NBS, alíquotas, CST, classificações
- ✅ Tipagem com Pydantic v2
- ✅ Suporte a context manager (`with`)
- ✅ 100% de cobertura de testes
- ✅ Skills em português e inglês

## Instalação

```bash
pip install receita-federal-client
```

## Início rápido

```python
from receita_federal_client import ReceitaFederalClient, ReceitaFederalClientConfig

config = ReceitaFederalClientConfig(base_url="http://localhost:8082")

with ReceitaFederalClient(config) as client:
    # Simples Nacional
    simples = client.simples_nacional.calcular({
        "cnpj": "12345678000190",
        "valor_operacao": 1000.00,
        "c_class_trib": "01",
        "data": "2025-01-15",
    })

    # DANFSe
    pdf = client.danfse.gerar_pdf({"xml_nfse": xml_nfse})
```

## Testes

```bash
pip install -e ".[dev]"
pytest
```

Cobertura exigida: 100%.

## Repositórios oficiais

- Simples Nacional: https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional
- Regime Geral: https://github.com/ReceitaFederal/calculadora-rtc-regime-regular
- DANFSe: https://github.com/ReceitaFederal/calculadora-rtc-gerador-danfse

Este cliente é mantido no ecossistema https://github.com/GambiarraFinance.

## Licença

MIT
