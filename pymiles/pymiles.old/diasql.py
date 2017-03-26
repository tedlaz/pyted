#    PyDia SQL.py : SQL dump.
# Copy it to /usr/share/dia/python

import dia
# import sys
import os
import string
import re
import datetime


class SQLRenderer:

    def __init__(self):
        self.f = None

    def begin_render(self, data, filename):
        self.f = open(filename, "w")
        name = os.path.split(filename)[1]
        self.f.write('''BEGIN TRANSACTION;\n''')
        for layer in data.layers:
            self.WriteTables(layer)

    def WriteTables(self, layer):
        tables = {}
        appdata = 'appdata'
        priority = {'fields': 0, 'foreign_keys': 100}
        # value for id
        z = ["INSERT INTO zf VALUES ('id', 'No', 'INTEGER', '1');"]
        z.append("INSERT INTO z VALUES('diadate', '%s');" % datetime.date.today().isoformat())
        zsql = "INSERT INTO z VALUES('%s', '%s');"
        zfsql = "INSERT INTO zf VALUES ('%s', '%s', '%s', '%s');"
        ztsql = "INSERT INTO zt VALUES ('%s', '%s', '%s', '%s');"

        for o in layer.objects:
            if o.type.name == 'Database - Table':
                if "name" in o.properties.keys():
                    table = o.properties["name"].value
                elif "text" in o.properties.keys():
                    table = o.properties["text"].value.text
                else:
                    continue
                if len(table) == 0 or string.find(table, " ") >= 0:
                    continue
                if table not in tables.keys():
                    tables[table] = ''
                if table == appdata:
                    attrs = o.properties['attributes'].value
                    for attr in attrs:
                        z.append(zsql % (attr[0], attr[1]))
                    continue
                # zt.append(comment)
                # first line is label
                # second line is label plural
                # third line is rpr
                clst = o.properties['comment'].value.split('\n')
                if len(clst) >= 3:
                    z.append(ztsql % (table, clst[0], clst[1], clst[2]))
                atributes = o.properties['attributes'].value
                for i in range(0, len(atributes)):
                    a = atributes[i]
                    if a[0] == 'id':
                        tables[table] = '%0.3d\tid INTEGER PRIMARY KEY\n' %\
                            (priority['fields'] + i)
                        continue
                    if len(a[0]) > 4:
                        if a[0][-3:] == '_id':
                            nnul = ''
                            if a[4] == 0:
                                nnul = ' NOT NULL'
                            tables[table] += '%0.3d\t%s INTEGER%s REFERENCES %s(id)\n' % (priority['fields'] + i, a[0], nnul, a[0][:-3])
                            continue
                    tipo = ''
                    if re.match('.*enum\(.*', a[1], re.I):
                        tipo = a[1]
                    else:
                        tipo = a[1].upper()
                    if tipo == '':
                        tipo = 'TEXT'
                    tables[table] += '%0.3d\t%s %s' % (priority['fields'] + i, a[0], tipo)
                    if a[3] == 1:
                        tables[table] += ' PRIMARY KEY'

                    if a[4] == 0:
                        if a[3] != 1:
                            tables[table] += ' NOT NULL'
                            notnull = 1
                    else:
                        tables[table] += ''
                        notnull = 0

                    if a[5] == 1:
                        if a[3] != 1:
                            tables[table] += ' UNIQUE'

                    # Create insert for table zflbl
                    if (len(a[2]) > 0):
                        z.append(zfsql % (a[0], a[2], tipo, notnull))

                    tables[table] += '\n'
            elif o.type.name == 'Database - Reference':
                continue
        for k in sorted(tables.keys()):
            # self.f.write('\n-- %s --\nDROP TABLE IF EXISTS `%s`;\n' % (k,k) )
            if k != appdata:
                self.f.write('CREATE TABLE IF NOT EXISTS %s (\n' % k)
                sentences = sorted(tables[k].split('\n'))
                sentences = [str(s[3:]) for s in sentences if len(s) > 4]
                sentences = ",\n".join(sentences)
                self.f.write('%s\n' % sentences)
                self.f.write(');\n')
        self.f.write('CREATE TABLE IF NOT EXISTS z (key TEXT PRIMARY KEY, val TEXT NOT NULL);\n')
        self.f.write('CREATE TABLE IF NOT EXISTS zt (tbl TEXT PRIMARY KEY, tlbl TEXT NOT NULL UNIQUE, tlblp TEXT NOT NULL UNIQUE, rpr TEXT NOT NULL);\n')
        self.f.write('CREATE TABLE IF NOT EXISTS zf (fld TEXT PRIMARY KEY, flbl TEXT NOT NULL UNIQUE, typos TEXT NOT NULL, nonull INTEGER NOT NULL DEFAULT 1);\n')

        self.f.write('\n'.join(sorted(z)))
        self.f.write('\n')

    def end_render(self):
        self.f.write('COMMIT;\n')
        self.f.close()

# reference
dia.register_export("PyDia SQL generator", "sql", SQLRenderer())
