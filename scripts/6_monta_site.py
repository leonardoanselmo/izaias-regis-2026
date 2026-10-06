"""Junta os dados dos passos 1 a 5 e gera o site (index.html na raiz do repositório).

Saídas: dados/relatorio.json (tudo o que a página usa) e index.html
"""
import csv

from comum import CANDIDATO, DADOS, RAIZ, ler_json, salvar_json

estado = ler_json('resultado_estado.json')
cargo = estado['carg'][0]
psd = next(p for a in cargo['agr'] for p in a['par'] if p['n'] == '55')
gar = ler_json('garanhuns.json')

with open(DADOS / 'izaias_regis_5567_por_municipio.csv', encoding='utf-8-sig') as f:
    mun = [[r[0], int(r[1]), float(r[2].replace(',', '.'))] for r in list(csv.reader(f, delimiter=';'))[1:]]

relatorio = dict(
    meta=dict(dg=estado['dg'], hg=estado['hg'], aviso=estado.get('mntf', ''), qe=int(cargo['qe'])),
    mun=[r for r in mun if r[1] > 0],
    mapa=ler_json('mapa.json'),
    psd=[dict(n=k['n'], nm=k['nmu'], v=int(k['vap'])) for k in sorted(psd['cand'], key=lambda k: -int(k['vap']))[:12]],
    psdTot=int(psd['tvtn']) + int(psd['tvtl']),
    seats=sorted([dict(nm=x['com'], v=x['v'], s=x['s']) for x in ler_json('cadeiras.json') if x['s'] > 0], key=lambda x: -x['v']),
    comp=ler_json('comparacao_2022.json'),
    secoes=ler_json('secoes.json'),
    gar=dict(validos=gar['validos'], brancos=gar['brancos'], nulos=gar['nulos'], top=gar['top'][:10], bairros=gar['bairros'],
             locais=[{k: v for k, v in l.items() if k not in ('lat', 'lon')} for l in gar['locais']]),
)
salvar_json(relatorio, 'relatorio.json')

modelo = (RAIZ / 'scripts' / 'template.html').read_text(encoding='utf-8')
geo = (DADOS / 'pe_municipios.geojson').read_text(encoding='utf-8')
dados = (DADOS / 'relatorio.json').read_text(encoding='utf-8')
corpo = modelo.replace('/*DATA*/', dados).replace('/*GEO*/', geo)
# o modelo começa no <title> e termina no </script>; aqui vira um documento HTML completo
cabeca, resto = corpo.split('</style>', 1)
html = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        + cabeca + '</style></head><body>' + resto + '</body></html>\n')
(RAIZ / 'index.html').write_text(html, encoding='utf-8')
print(f'index.html gerado ({len(html) // 1024} KB), dados do TSE de {estado["dg"]} {estado["hg"]}')
