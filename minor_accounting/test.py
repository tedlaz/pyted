import itertools
SYNTELESTES = [0.24, 0.13, 0.17]
SYNTNAMES = ['24', '13', '17']


def match(arthro_dic, thres=0.02):
    vals = [20, 100, 100]
    vat = [24.01, 13, 4.8]
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
            key = '%s%s' % (j, SYNTNAMES[pair_scor.index(minv)])
            hand_score[key] = minv
        scores.append(hand_score)
        scval.append(htot)
    print(scores)
    print(scval)
    best_index = scval.index(min(scval))
    print(best_index, comp[best_index], scores[best_index])
    print("error: %.2f" % sum(scores[best_index].values()))
    lvals = len(vals)
    lvat = len(vat)
    # Όταν τα φπα είναι περισσότερα από τις τιμές υπάρχει λάθος
    if lvals < lvat:
        raise Exception("Vat more than vals")
    if lvals == 1:
        if lvat == 1:
            for pvat in SYNTELESTES:
                if abs(vat[0] - vals[0] * pvat) < thres:
                    return True
    return False


if __name__ == "__main__":
    arthro = {'20.00.2024': 100, '54.00.2024': 24, '50.00': -124}
    print(match(arthro))
