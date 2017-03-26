# -*- coding: utf-8 -*-
'''
Created on 31 Μαρ 2014

@author: tedlaz
'''
name  = 'testSql'
label = u'Δοκιμαστική ερώτηση'
sql = """\
SELECT * 
FROM ert
INNER JOIN tbl1 ON tbl1.id = id
"""
if __name__ == '__main__':
    print sql