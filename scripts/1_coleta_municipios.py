"""Coleta os votos do candidato 5567 em cada município de PE pela API de resultados do TSE.

Saídas em dados/:
  resultado_estado.json                 resultado estadual completo de deputado federal (todos os candidatos)
  izaias_regis_5567_por_municipio.csv   votos e % dos válidos em cada um dos 185 municípios
"""
import concurrent.futures as cf
import csv
import json

from comum import API, CANDIDATO, DADOS, ELEICAO, UF, get_json, municipios_pe, salvar_json

BASE = f'{API}/{ELEICAO}/dados/{UF}/'


def acha_candidato(d, num=CANDIDATO):
    for cargo in d['carg']:
        if cargo['cd'] != '6':  # 6 = Deputado Federal
            continue
        for a in cargo['agr']:
            for p in a['par']:
                for k in p.get('cand', []):
                    if k['n'] == num:
                        return k, p


estado = get_json(f'{BASE}{UF}-c0006-e00{ELEICAO}-u.json')
salvar_json(estado, 'resultado_estado.json')
k, p = acha_candidato(estado)
print(f"{k['nm']} ({p['sg']}): {k['vap']} votos, {k['pvap']}%, {k['seq']}º lugar")
print(f"Dados do TSE de {estado['dg']} {estado['hg']}. Aviso: {estado.get('mntf') or '(nenhum)'}")

mun = municipios_pe()


def um(m):
    d = get_json(f"{BASE}{UF}{m['cd']}-c0006-e00{ELEICAO}-u.json")
    k, _ = acha_candidato(d)
    return m['nm'], int(k['vap']), float(k['pvap'].replace(',', '.'))


with cf.ThreadPoolExecutor(12) as ex:
    linhas = sorted(ex.map(um, mun), key=lambda r: -r[1])

with open(DADOS / 'izaias_regis_5567_por_municipio.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['Municipio', 'Votos', '% votos validos no municipio'])
    for nome, votos, pct in linhas:
        w.writerow([nome, votos, str(pct).replace('.', ',')])

total = sum(r[1] for r in linhas)
print(f'{len(linhas)} municípios, {total} votos (estado: {k["vap"]}), {sum(1 for r in linhas if r[1])} com voto')
assert total == int(k['vap']), 'soma por município não bate com o total do estado'
