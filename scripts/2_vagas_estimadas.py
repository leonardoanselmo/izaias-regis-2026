"""Estima a distribuição das 25 vagas de deputado federal em PE.

Enquanto o TSE não proclama os eleitos, recalcula a partir dos votos publicados:
  1. quociente partidário = votos da agremiação // quociente eleitoral (QE),
     limitado aos candidatos com pelo menos 10% do QE;
  2. sobras pela maior média, só para agremiações com 80% do QE e candidatos com 20% do QE.
É uma estimativa: o resultado oficial é o que o TSE proclamar.

Entrada: dados/resultado_estado.json (passo 1). Saída: dados/cadeiras.json
"""
from comum import ler_json, salvar_json

estado = ler_json('resultado_estado.json')
cargo = estado['carg'][0]
QE, NV = int(cargo['qe']), int(cargo['nv'])

ags = []
for a in cargo['agr']:
    votos, cands = 0, []
    for p in a['par']:
        votos += int(p.get('tvtn', 0)) + int(p.get('tvtl', 0))
        cands += [(int(k['vap']), k['nmu'], p['sg']) for k in p.get('cand', []) if k['dvt'].startswith('V')]
    cands.sort(reverse=True)
    elegiveis = [k for k in cands if k[0] >= 0.1 * QE]
    ags.append(dict(nm=a['nm'], com=a['com'], v=votos, c=cands, s=min(votos // QE, len(elegiveis))))

print(f'QE {QE}, {NV} vagas, válidos {sum(x["v"] for x in ags)}')
vagas = sum(x['s'] for x in ags)
while vagas < NV:
    melhor = None
    for x in ags:
        if x['v'] < 0.8 * QE:
            continue
        if not [k for k in x['c'][x['s']:] if k[0] >= 0.2 * QE]:
            continue
        media = x['v'] / (x['s'] + 1)
        if melhor is None or media > melhor[0]:
            melhor = (media, x)
    if not melhor:
        break
    melhor[1]['s'] += 1
    vagas += 1

for x in sorted(ags, key=lambda x: -x['v']):
    if x['s']:
        print(f"{x['com']:<20} {x['v']:>9}  {x['s']} vaga(s)  último eleito: {x['c'][x['s'] - 1]}")

# votos a mais que o PSD precisaria para uma 3ª vaga: superar a menor média que ganhou uma sobra
medias = [x['v'] / x['s'] for x in ags if x['s'] > x['v'] // QE]
psd = next(x for x in ags if x['com'] == 'PSD')
print(f"PSD precisaria de ~{min(medias) * (psd['s'] + 1) - psd['v']:.0f} votos a mais para a {psd['s'] + 1}ª vaga")

salvar_json([{k: x[k] for k in ('nm', 'com', 'v', 's')} | {'eleitos': x['c'][:x['s']]} for x in ags], 'cadeiras.json')
