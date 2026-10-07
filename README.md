# Izaias Regis 5567 em 2026

Para onde foram os votos de Izaias Regis (PSD, número 5567) para deputado federal em Pernambuco, no 1º turno de 04/10/2026.

**Site:** https://leonardoanselmo.github.io/izaias-regis-2026/

O relatório tem:
- mapa de Pernambuco com os votos por município;
- os 106 municípios onde ele teve voto;
- comparação com 2022, quando ele foi eleito deputado estadual pelo PSDB (número 45678);
- Garanhuns por bairro e por local de votação;
- Garanhuns 2022 × 2026: onde Izaias perdeu espaço e Felipe Carreras cresceu, com mapa dos locais de votação;
- votos em cada seção eleitoral de PE, sem misturar as seções agregadas;
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
python 3b_votos_por_secao.py    # votos do 5567 em cada seção de PE (mesmos downloads do passo 3)
python 3c_garanhuns_2022.py     # Garanhuns 2022 x 2026 por bairro e local (~150 MB de 2022)
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

## Seções agregadas e consolidadas

Quando uma seção é agregada a outra, os eleitores dela votam na urna da seção principal, e o TSE publica o resultado só na principal. O arquivo de votos por seção não tem linhas para as agregadas: em PE são 673 agregadas, somadas em 626 seções principais.

Por isso, o passo 3b:
- não cria linha para seção agregada (e confere que nenhuma agregada tem voto próprio);
- marca a principal como consolidada e lista as agregadas que ela recebe;
- soma o eleitorado da principal com o das agregadas, para o percentual não misturar bases.

O arquivo de locais de votação repete cada seção para o 1º e o 2º turno, e o mesmo código de local pode apontar para outro prédio no 2º turno. Os scripts usam só as linhas do 1º turno e ligam cada seção ao local pela própria seção, não pelo código do local.

O resultado está em `dados/izaias_regis_5567_por_secao.csv`: todas as 21.418 seções com resultado em PE, inclusive as com 0 votos.

## Fontes

- [API de resultados do TSE](https://resultados.tse.jus.br/oficial/ele2026/6259/dados/pe/pe-c0006-e006259-u.json): votos por município em 2026 (eleição 6259, cargo 6).
- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/): `votacao_secao_2026_PE`, `eleitorado_local_votacao_2026` e `votacao_candidato_munzona_2022`.
- Contornos dos municípios: [geodata-br](https://github.com/tbrugz/geodata-br), a partir da malha do IBGE.

## Sobre o PDF

As dicas ao passar o mouse no PDF aparecem no Adobe Acrobat Reader e no Firefox. O leitor de PDF do Chrome e do Edge não as mostra. Para a versão interativa em qualquer navegador, use o site.

---

## Quem desenvolveu?

<img src="img/leo.jpg" alt="Foto de Léo Ansélmo" width="96" align="left">

**Léo Ansélmo** — Bacharelado em Administração e Desenvolvimento de Sistemas, com mais de 20 anos de experiência na área.

Procurei desenvolver um relatório baseado nos dados do TSE, mostrando o panorama político do candidato para o mesmo entender os dados consolidados e gerar conhecimento agregado da campanha atual.

Com ajuda da inteligência artificial (AI) nos mapas e gráficos, obtendo uma compreensão visual mais detalhada.

Instagram: [@leonardoanselmo79](https://www.instagram.com/leonardoanselmo79/)
