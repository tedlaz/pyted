"""
Testing module
"""
import symbasi as sm


if __name__ == "__main__":
    SYM1 = sm.Symbasi(sm.AORISTOY, sm.MISTHOS, 344.52)
    print(SYM1)
    SYM2 = sm.Symbasi(sm.AORISTOY, sm.IMEROMISTHIO, 26.18, 3, 19)
    print(SYM2)
    print(SYM2.calc_apod(10))
    SYM2.check()
    print(SYM2.calc_misthos(40))
