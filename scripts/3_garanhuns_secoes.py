"""Garanhuns em detalhe: ranking de candidatos, votos por bairro e por local de votação.

Baixa do Portal de Dados Abertos do TSE (para brutos/, ~280 MB no total):
  votacao_secao_2026_PE.zip           votos por seção eleitoral
  eleitorado_local_votacao_2026.zip   locais de votação com bairro e coordenadas
Saída: dados/garanhuns.json
"""
import collections as C
import csv
import io
import zipfile

from comum import BRUTOS, CANDIDATO, CDN, baixar, salvar_json

MUNICIPIO = 'GARANHUNS'


def linhas_do_municipio(zip_path, membro):
    with zipfile.ZipFile(zip_path) as z, z.open(membro) as f:
        r = csv.DictReader(io.TextIOWrapper(f, encoding='latin-1'), delimiter=';')
        yield from (row for row in r if row['NM_MUNICIPIO'] == MUNICIPIO)


secao_zip = baixar(f'{CDN}/votacao_secao/votacao_secao_2026_PE.zip', BRUTOS / 'votacao_secao_2026_PE.zip')
locais_zip = baixar(f'{CDN}/eleitorado_locais_votacao/eleitorado_local_votacao_2026.zip', BRUTOS / 'eleitorado_local_votacao_2026.zip')

fed = [r for r in linhas_do_municipio(secao_zip, 'votacao_secao_2026_PE.csv') if r['CD_CARGO'] == '6']
locais = {r['NR_LOCAL_VOTACAO']: r for r in linhas_do_municipio(locais_zip, 'eleitorado_local_votacao_2026_PE.csv')}

# ranking na cidade (95 = branco, 96 = nulo; números de 4 dígitos = candidatos)
tot, nomes = C.Counter(), {}
for r in fed:
    tot[r['NR_VOTAVEL']] += int(r['QT_VOTOS'])
    nomes[r['NR_VOTAVEL']] = r['NM_VOTAVEL']
validos = sum(v for k, v in tot.items() if k not in ('95', '96'))
nominais = sorted(((v, k, nomes[k]) for k, v in tot.items() if len(k) == 4), reverse=True)
print(f'válidos {validos}, brancos {tot["95"]}, nulos {tot["96"]}, candidato {tot[CANDIDATO]}')

# por local de votação
por_local = C.defaultdict(lambda: {'votos': 0, 'validos': 0, 'secoes': set(), 'nome': ''})
for r in fed:
    x = por_local[r['NR_LOCAL_VOTACAO']]
    x['nome'] = r['NM_LOCAL_VOTACAO']
    x['secoes'].add(r['NR_SECAO'])
    if r['NR_VOTAVEL'] not in ('95', '96'):
        x['validos'] += int(r['QT_VOTOS'])
    if r['NR_VOTAVEL'] == CANDIDATO:
        x['votos'] += int(r['QT_VOTOS'])

saida_locais = []
for nr, x in por_local.items():
    loc = locais.get(nr, {})
    saida_locais.append(dict(local=x['nome'], bairro=loc.get('NM_BAIRRO', ''), lat=loc.get('NR_LATITUDE', ''),
                             lon=loc.get('NR_LONGITUDE', ''), secoes=len(x['secoes']), votos=x['votos'],
                             validos=x['validos'], pct=round(100 * x['votos'] / x['validos'], 2) if x['validos'] else 0))
saida_locais.sort(key=lambda x: -x['votos'])

por_bairro = C.defaultdict(lambda: [0, 0])
for l in saida_locais:
    por_bairro[l['bairro']][0] += l['votos']
    por_bairro[l['bairro']][1] += l['validos']
bairros = sorted(([b, a, v, round(100 * a / v, 2)] for b, (a, v) in por_bairro.items()), key=lambda x: -x[1])

print(f'{len(saida_locais)} locais, {len({r["NR_SECAO"] for r in fed})} seções, {len(bairros)} bairros')
salvar_json(dict(validos=validos, brancos=tot['95'], nulos=tot['96'],
                 top=[dict(n=k, nm=n, v=v, p=round(100 * v / validos, 2)) for v, k, n in nominais[:15]],
                 locais=saida_locais, bairros=bairros), 'garanhuns.json')
