from elee import parsers
from elee import arthro_categories as ac
logariasmoi, arthra = parsers.parse_el('el2017.txt')

for arthro in arthra:
    # if arthro.category(ac.lca) == 'ERROR':
    print(arthro)
    print(arthro.category(ac.lca))
