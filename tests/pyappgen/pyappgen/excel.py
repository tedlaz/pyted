# -*- coding: utf-8 -*-
'''
Created on 5 Φεβρουαρίου 2014

@author: tedlaz
'''
import xlwt
h = [u'Δοκιμή',u'Αξία',u'Τεστ']
arr = [[u'Δοκιμή1',100,'ssdfg'],[u'Δοκιμή2',200,'ssdf'],[u'Δοκιμή3',300,'sdf'],[u'Δοκιμή4',400,'sdf']]

def makeExcelFile(values,headers,fname):
    w  = xlwt.Workbook()
    tst_style = xlwt.easyxf('pattern: pattern solid, fore_color blue; font:  bold 1, color white; align: horiz center, vert center;')# border: top thick, right thick, bottom thick, left thick;')

    nstyle = xlwt.easyxf(num_format_str='#,##0.00')
    ws = w.add_sheet('s1')
    #write headers 
    for el in enumerate(headers):
        ws.write(0,el[0],el[1],tst_style)
    #write values
    for row in enumerate(values):
        for col in enumerate(row[1]):
            ws.write(row[0]+1,col[0],col[1],nstyle)
    w.save(fname)
    print 'ok'

if __name__ == "__main__":
    import dbutils as dbu
    sql = "SELECT id,epon,onom,patr,mitr,igen FROM m12_fpr"
    arr1,h1 = dbu.getDbRows(sql, 'E:/Dropbox/mis.m13')
    fname = 'C:/Users/tedlaz/Desktop/tst.xls'
    makeExcelFile(arr1,h1,fname)