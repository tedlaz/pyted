import stamatis as s
basis = s.dec('1.1231123173',10)
gap = s.dec('0.005',10)
num   = '11.2311231230'
ar = []
r = range(1000)
x = []
ix = [] 
tbas = basis
for i in r:
    l = s.findLowerUpperHarmonic(tbas,num)[4]
    ar.append(l)
    x.append(tbas)
    ix.append(tbas-l)
    tbas = tbas+gap
import numpy as np
import matplotlib.pyplot as plt
plt.plot(x,ar,x,ix)
plt.show()
