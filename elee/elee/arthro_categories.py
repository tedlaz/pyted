"""
Ακολουθεί dictionary με κανόνες για την ταξινόμηση λογιστικών εγγραφών
Πάνω πάνω είναι οι πιο ειδικοί κανόνες
στο τέλος οι πιο γενικοί
Όταν γίνει ταυτοποίηση ενός κανόνα έχουμε τερματισμό
"""
lca = {
    'poliseisMeFpa': set(('7:2', '54.00:2', '30:1')),
    'akyrotikoPoliseonMeFpa': set(('3:-1', '7:-2', '54.00:-2')),
    'poliseisXorisFpa': set(('7:2', '30:1')),
    'agoresPagion': set(('1:1', '54.00:1', '5:2')),
    'agoresEpiPistosei': set(('2:1', '54.00:1', '50.00:2')),
    'agoresEndokoinotikes': set(('2:1', '50.01:2')),
    'pistotikoAgores': set(('2:-1', '54.00:-1', '50:-2')),
    'agoresMetrita': set(('2:1', '54.00:1', '38:2')),
    'misthodosia': set(('60:1', '53:2', '55:2')),
    'ejodaMeFpaEpiPistosei': set(('6:1', '54.00.29:1', '5:2')),
    'ejodaMeFpaEpiPistoseiPistotiko': set(('6:-1', '54.00.29:-1', '5:-2')),
    'ejodaMeFpaMetrita': set(('6:1', '54.00.29:1', '3:2')),
    'ejodaXorisFpaMetrita': set(('6:1', '38:2')),
    'trapezikaEjoda': set(('38.03:2', '65:1')),
    'trapezikaEjodaDaneiakoy': set(('52:2', '65:1')),
    'enantiLogariasmoyProsopiko': set(('38:2', '53.00:1')),
    'enantiLogariasmoy': set(('38:2', '5:1')),
    'plhromiIka': set(('38.03:2', '55.00:1')),
    'eisprajiApoPelati': set(('30.00:2', '38:1')),
    'metafora': set(('38:1', '38:2')),
    'metaforaDaneiakon': set(('52:1', '52:2')),
    'sympsifismosPromithefton': set(('53:1', '53:2')),
    'ejodaXorisFpaEpiPistosei': set(('6:1', '5:2')),
    'aposbeseis': set(('66:1', '1:2')),
    'epistrofiMetritaSePelati': set(('30:-2', '38:-1')),
    'pistotikoiTokoi': set(('38:-2', '65:-1')),
    'epistrofiMetritonApoPromithefti': set(('38:1', '5:2')),
    'epistrofiMetritonApoPromitheftip': set(('50:-1', '38:-2')),
    'AgoresEndokoinotikesWindhager': set(('50:2', '20.01.00.000:1', '24:1'))
}
