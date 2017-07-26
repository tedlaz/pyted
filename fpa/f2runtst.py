# *- coding: utf-8 -*
import f2run
import os

FDIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    EPON = u'Σαμαράς ΟΕ'
    DBF = '/home/tedlaz/pelates/2017/b/2017b.sql3'
    HTMLF = '/home/tedlaz/pelates/2017/b/2017b.html'
    TMPLF = os.path.join(FDIR, '1tmpl.txt')
    LMOIF = os.path.join(FDIR, '2lmoi.txt')
    FIS = os.path.join(FDIR, './3is.sql')
    FFP = os.path.join(FDIR, '4fpa.sql')
    f2run.run(EPON,
              '2017-04-01',
              '2017-06-30',
              DBF,
              HTMLF,
              TMPLF,
              LMOIF,
              FIS,
              FFP)
    f2run.checkDictionaries(TMPLF, LMOIF)
    import webbrowser
    webbrowser.get('chromium %s').open(HTMLF)
