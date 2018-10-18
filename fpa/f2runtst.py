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


def runit(dbf, xrisi, period=None, ypoloipo=0):
    EPO = u'Σαμαράς ΟΕ'
    dname = os.path.dirname(os.path.abspath(dbf))
    HTMLF = dname + ('/fpa%s%s.html' % (xrisi, period))
    papo = '%s-01-01' % xrisi
    peos = '%s-12-31' % xrisi
    if period in 'aA':
        papo = '%s-01-01' % xrisi
        peos = '%s-03-31' % xrisi
    elif period in 'bB':
        papo = '%s-04-01' % xrisi
        peos = '%s-06-30' % xrisi
    elif period in 'cC':
        papo = '%s-07-01' % xrisi
        peos = '%s-09-30' % xrisi
    elif period in 'bB':
        papo = '%s-10-01' % xrisi
        peos = '%s-12-31' % xrisi
    #print(EPO, HTMLF, papo, peos, period, ypoloipo)
    main(EPO, dbf, HTMLF, papo, peos, ypoloipo)


if __name__ == '__main__':
    DBF = '/home/ted/tmp/fpa/2018.sql3'
    HTMLF = '/home/ted/tmp/fpa/2018c.html'
    runit(DBF, '2018', 'c', 0)
