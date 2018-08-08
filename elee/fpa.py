from elee import arthro
ar1 = arthro.Arthro('2018-01-01', 'TDA123', 'Agores')
ar1.add_line('30.00.00', 124, 0)
ar1.add_line('70.00.24', 0, 100)
ar1.add_line('54.00.24', 0, 24)
ar1.add_line('70.00.24', 0, 100)
ar1.add_line('54.00.24', 0, 24)
ar1.add_line('30.00.00', 124, 0)
ar1.add_line('70.01.13', 0, 100)
ar1.add_line('54.00.13', 0, 12.79)
ar1.add_line('30.00.00', 112.79, 0)
print(ar1.check_fpa())

