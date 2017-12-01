"""TESTING data2text.py"""
import unittest
import data2text as d2t


class TestData2text(unittest.TestCase):
    def test_Col(self):
        self.assertEqual(d2t.Col('epo', 10).txt('ted') , 'ted       ')
        self.assertEqual(d2t.Col('epo', 5, ' ', 2).txt('ted'), '  ted')
        self.assertEqual(d2t.Col('epo', 5, '+', 2).txt('ted'), '++ted')

    def test_gen(self):
        row1 = d2t.Row(2)
        row1.acol(d2t.ColCap('epo', 30))
        row1.acol(d2t.ColDec('ika', 12, 0))
        row1.acol(d2t.ColDec('poso', 12))
        row2 = d2t.Row('eof')
        rowa = d2t.Row(1)
        rowa.acol(d2t.Col('per', 8))
        rowa.acol(d2t.Col('xri', 4))
        rowa.acol(d2t.ColCalc('e', 14, '2', 'ika'))
        rowa.acol(d2t.ColCalc('tposo', 14, '2', 'poso'))
        doc = d2t.Doc([rowa, row1, row2])
        # doc.add_rowtype(row1)
        # doc.add_rowtype(row2)
        doc.add_row(1, {'per': '20170101', 'xri': '2017', 'tposo': 0, 'e': ''})
        doc.add_row(2, {'epo': 'Λάζαρος', 'ika': 20, 'poso': 100})
        doc.add_row(2, {'epo': 'Μαραβελιας', 'ika': 20, 'poso': 120.38})
        doc.add_row(2, {'epo': 'Μαραβελιας', 'ika': 20, 'poso': 30})
        for i in range(10):
            doc.add_row(2, {'epo': 'Λάζαρος', 'ika': 15, 'poso': 100})
        doc.add_row('eof', {})
        ftxt = doc.txt
        print(ftxt)
        print(doc.txt2dics(ftxt))
        # filen = '/home/tedlaz/malakia.txt'
        # enc = 'CP1253'  # 'UTF-8'
        # doc.save2file(filen, enc)
        # print('+' * 80)
        # print(doc.from_file(filen, enc))
        # print('+' * 80)
