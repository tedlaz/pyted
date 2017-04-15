"""
Tests here
"""
import unittest
import os
import textdata as td


def setUpModule():
    pass


def tearDownModule():
    print('edo telos')


class Test_textdata(unittest.TestCase):
    def test_a1(self):
        lerg = td.Linetype('erg', 1)
        lerg.add_field(td.Field('epo', td.TL, 30))
        lerg.add_field(td.Field('ono', td.TL, 30))
        print(lerg)
        lerd = td.Linetype('ergd', 2)
        lerd.add_field(td.Field('apo', td.D, 10))
        lerd.add_field(td.Field('eos', td.D, 10))
        lerd.add_field(td.Field('poso', td.N, 12))
        lerd.add_field(td.Field('fmy', td.N, 12))
        print(lerd)
        eof = td.Linetype('End', 'EOF')
        te = td.Text_data()
        te.add_linetype(lerg)
        te.add_linetype(lerd)
        te.add_linetype(eof)
        strr = ''
        strr += '%s\n' % te.add_txtline(1, ['ted', 'laz'])
        strr += '%s\n' % te.add_txtline(2, ['2016-01-01', '2016-01-31', 100.32, 10])
        strr += '%s\n' % te.add_txtline(2, ['2016-01-01', '2016-01-31', 365, 11.11])
        strr += '%s\n' % te.add_txtline('EOF', [])
        print(strr)
        fil = '/home/tedlaz/tst.txt'
        te.write(fil, strr)
        print(te.read(fil))
        os.remove(fil)
