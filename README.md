# Izaias Regis 5567 em 2026

Para onde foram os votos de Izaias Regis (PSD, número 5567) para deputado federal em Pernambuco, no 1º turno de 04/10/2026.

**Site:** https://leonardoanselmo.github.io/izaias-regis-2026/

O relatório tem:
- mapa de Pernambuco com os votos por município;
- os 106 municípios onde ele teve voto;
- comparação com 2022, quando ele foi eleito deputado estadual pelo PSDB (número 45678);
- Garanhuns por bairro e por local de votação;
- estimativa de quantos votos faltaram para a vaga.

> Os dados de 2026 vêm da totalização do TSE, que ainda mostra o aviso "Aguarde reprocessamento da eleição". Os números podem mudar. A distribuição de vagas é uma estimativa própria, e o resultado oficial é o que o TSE proclamar.

## Estrutura

| Pasta / arquivo | Conteúdo |
|---|---|
| `index.html` | O site publicado no GitHub Pages (gerado pelo passo 6) |
| `scripts/` | Coleta e análise, numeradas na ordem em que rodam |
| `scripts/template.html` | Modelo da página. Os dados são inseridos no passo 6 |
| `dados/` | Resultados pequenos que alimentam o site e o PDF |
| `relatorio/` | Versão em PDF (gerada pelo passo 7) |
| `brutos/` | Downloads grandes do TSE (fora do Git, criados pelos scripts) |

## Como atualizar

Requer Python 3.10 ou mais novo. Os passos 1 a 6 usam só a biblioteca padrão.

```bash
cd scripts
python 1_coleta_municipios.py   # API do TSE: votos do 5567 nos 185 municípios
python 2_vagas_estimadas.py     # estimativa das 25 vagas (quociente eleitoral e sobras)
python 3_garanhuns_secoes.py    # votos por seção e locais de votação de Garanhuns (~280 MB)
python 4_comparacao_2022.py     # votos de 2022 por município (~640 MB na 1ª vez)
python 5_mapa.py                # contornos dos municípios e votos por código IBGE
python 6_monta_site.py          # gera dados/relatorio.json e index.html
```

Para gerar o PDF:

```bash
pip install -r requirements.txt
python scripts/7_gera_pdf.py
```

Os arquivos grandes ficam em `brutos/` e só são baixados se ainda não existirem. Para pegar uma versão nova da votação por seção, apague o arquivo correspondente em `brutos/` antes de rodar o passo 3.

Depois de atualizar, publique com `git add -A && git commit && git push`. O GitHub Pages atualiza o site no mesmo endereço em um ou dois minutos.

## Fontes

- [API de resultados do TSE](https://resultados.tse.jus.br/oficial/ele2026/6259/dados/pe/pe-c0006-e006259-u.json): votos por município em 2026 (eleição 6259, cargo 6).
- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/): `votacao_secao_2026_PE`, `eleitorado_local_votacao_2026` e `votacao_candidato_munzona_2022`.
- Contornos dos municípios: [geodata-br](https://github.com/tbrugz/geodata-br), a partir da malha do IBGE.

## Sobre o PDF

As dicas ao passar o mouse no PDF aparecem no Adobe Acrobat Reader e no Firefox. O leitor de PDF do Chrome e do Edge não as mostra. Para a versão interativa em qualquer navegador, use o site.

---

Desenvolvido pelo Engenheiro de IA Léo Ansélmo
