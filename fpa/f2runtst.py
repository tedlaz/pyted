# *- coding: utf-8 -*
import f2run
import os

fdir = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    epon = u'Σαμαράς ΟΕ'
    db = '/home/tedlaz/tedfiles/prj/2017/2017a.sql3'
    htmlf = '/home/tedlaz/f2_tst.html'
    tmplfile = os.path.join(fdir, '1tmpl.txt')
    lmoifile = os.path.join(fdir, '2lmoi.txt')
    fis = os.path.join(fdir, './3is.sql')
    ffp = os.path.join(fdir, '4fpa.sql')
    f2run.run(epon,
              '2017-01-01',
              '2017-03-31',
              db,
              htmlf,
              tmplfile,
              lmoifile,
              fis,
              ffp)
    f2run.checkDictionaries(tmplfile, lmoifile)
    import webbrowser
    webbrowser.get('/usr/bin/google-chrome-stable %s').open(htmlf)
