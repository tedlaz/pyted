# *- coding: utf-8 -*
import f2run
import os

FDIR = os.path.dirname(os.path.abspath(__file__))


def main(epo, dbf, htmlf, apo, eos, ypo=0):
    TMPLF = os.path.join(FDIR, '1tmpl.txt')
    LMOIF = os.path.join(FDIR, '2lmoi.txt')
    FIS = os.path.join(FDIR, './3is.sql')
    FFP = os.path.join(FDIR, '4fpa.sql')
    f2run.run(epo,
              apo,
              eos,
              dbf,
              htmlf,
              TMPLF,
              LMOIF,
              FIS,
              FFP,
              ypo)
    f2run.checkDictionaries(TMPLF, LMOIF)
    import webbrowser
    webbrowser.get('google-chrome-stable %s').open(htmlf)


if __name__ == '__main__':
    EPO = u'Σαμαράς ΟΕ'
    DBF = '/home/tedlaz/pelates/2017/d/2017d.sql3'
    HTMLF = '/home/tedlaz/pelates/2017/d/2017d.html'
    main(EPO, DBF, HTMLF, '2018-01-1', '2018-31-31', 0)
