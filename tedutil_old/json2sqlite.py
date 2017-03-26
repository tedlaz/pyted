# -*- coding: utf-8 -*-
import json
# import ted_sqlite as tsq
import sqlite3

ar = {'date': '2015-01-01', 'par': 'tda31', 'per': 'Test tran',
      'lin': [
       {'lmo': '38.00.000', 'lpe': 'Tameio', 'xr': 1, 'val': 23.45},
       {'lmo': '30.00.000', 'lpe': 'Πελάτες', 'xr': 0, 'val': 23.45}
      ]
      }

js = json.dumps(ar, ensure_ascii=False)

sqcr = 'create table if not exists a(id INTEGER PRIMARY KEY, mydata json);'
sqli = '''insert into a values (null, %s)''' % js
file = 'tttt.sql3'
print(js)
# tsq.script_on_new_db(file, sqcr)
con = sqlite3.connect(file)
con.execute('insert into a values (null, ?)', (js,))
cur = con.cursor()
con.commit()
cur.execute("select * from ?", ('a', ))
a = cur.fetchall()
cur.close()
con.close()
for line in a:
    jd = json.loads(line[1])
    print(jd['date'], jd['per'])
    for l in jd['lin']:
        print('  %s %s' % (l['lmo'], l['val']))
