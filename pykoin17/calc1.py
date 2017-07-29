import distribute
pei = [.12, .065, .055, .12, .065, .055, .12, .065, .055, .28]
pfi = [.3, .2, .17, .35, .25, .22, .35, .25, .22, .45]
peifi = []
ores = [29, 22, 7, 13, 13, 10, 17, 24, 30, 50]

for i, _ in enumerate(pei):
    peifi.append(distribute.dec(pei[i] * pfi[i], 5))

one_minus_peifi = 1 - sum(peifi)

ores_pei = []

for i, _ in enumerate(pei):
    ores_pei.append(pei[i] * ores[i])

pores_pei = distribute.distribute_per_cent(ores_pei, 5)
pores_pei_a = distribute.multiply(one_minus_peifi, pores_pei, 5)
to1 = distribute.asum(peifi, pores_pei_a, 5)
#print(one_minus_peifi)
# print(pores_pei, sum(pores_pei))
print(pores_pei_a)
print('')
print(to1, sum(to1))
print('')
tot = distribute.multiply(718.5, to1, 5)
totf = distribute.dis_round(tot)
print(sum(totf), totf)