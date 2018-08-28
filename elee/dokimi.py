from elee import parsers
from elee import arthro_categories as ac
logariasmoi, arthra = parsers.parse_el('el2017.txt')
tst = '%4s %4s %s %15s %30s %12s %10s %12s %1s'
i = 1
for arthro in arthra:
    # if arthro.category(ac.lca) == 'ERROR':
    # print(arthro)
    # print(arthro.category(ac.lca))
    # if not arthro.check_fpa():
    #     print(arthro)
    v = arthro.esej
    if v:
        print(tst % (i, v[0], v[1], v[2][:15], v[3][:30], v[5], v[6], v[7], v[8]))
        i += 1
