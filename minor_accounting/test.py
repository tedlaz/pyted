import itertools
from collections import namedtuple
from decimal import Decimal as dec
Fel = namedtuple('Fel', 'poso fpa synt err')
SYNTELESTES = [0.24, 0.13, 0.17]
SYNTNAMES = ['24', '13', '17']


def list_subtract(ls1, ls2):
    final = ls1[:]
    for elm in ls2:
        if elm in final:
            del final[final.index(elm)]
    return final


def match(vals, vat, thres=0.02):
    # Όταν τα φπα είναι περισσότερα από τις τιμές υπάρχει λάθος
    if len(vals) < len(vat):
        raise Exception("Vat more than vals")
    comp = [list(zip(x, vat)) for x in itertools.permutations(vals, len(vat))]
    scores = []
    scval = []
    for cmv in comp:
        hand_score = {}
        htot = 0.0
        for j, pair in enumerate(cmv):
            pair_scor = []
            for syn in SYNTELESTES:
                pair_scor.append(abs(pair[0] * syn - pair[1]))
            minv = min(pair_scor)
            htot += minv
            key = (j, SYNTNAMES[pair_scor.index(minv)])
            hand_score[key] = minv
        scores.append(hand_score)
        scval.append(htot)
    print(comp)
    print("\n")
    print(scores)
    print("\n")
    print(scval)
    best_index = scval.index(min(scval))
    print(best_index, comp[best_index], scores[best_index])
    print("Total error: %.2f" % sum(scores[best_index].values()))
    to_subtract = [i[0] for i in comp[best_index]]
    print(to_subtract)
    vals_without_vat = list_subtract(vals, to_subtract)
    print(vals_without_vat)
    finals = []
    for i, elm in enumerate(comp[best_index]):
        # print(list(scores[best_index].keys())[i])
        fpa = list(scores[best_index].keys())[i][1]
        err = scores[best_index][(i, fpa)]
        finals.append(Fel(elm[0], elm[1], fpa, err))
    for elm in vals_without_vat:
        finals.append(Fel(elm, 0, '0', 0))
    print(finals)
    aaa = {}
    for elm in finals:
        aaa[elm.synt] = aaa.get(elm.synt, [dec(0), dec(0), dec(0)])
        aaa[elm.synt][0] += round(dec(elm.poso), 2)
        aaa[elm.synt][1] += round(dec(elm.fpa), 2)
        aaa[elm.synt][2] += round(dec(elm.err), 2)
    print(aaa)
    print("-" * 60)


if __name__ == "__main__":
    for i in range(20):
        print(match([100], [24]))
    print(match([100, 105], [13.1]))
    print(match([100.77], [13.1]))
    # print(list_subtract([100, 100, 20], [20, 100, 4]))
