# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''

'''
fields must start with:
  b : True or False   
  i : Integer
  s : String Values
  j : Like s but masked to take digits as text input
  n : Numeric with two decimals field
  t : Text values 
  z : Integer Foreign key 
  c : Integer Foreign key combo box
  d : Date 
  e : Date or empty string 
  f : DateTime 
  w : String of form [1,1,1,1,1,0,0] (see specifications) 
'''

sqlTypes = {'b': 'INTEGER',
            'i': 'INTEGER',
            's': 'VARCHAR(30)',
            'j': 'VARCHAR(30)',
            'n': 'DECIMAL',
            't': 'TEXT',
            'z': 'INTEGER',
            'c': 'INTEGER',
            'd': 'DATE',
            'e': 'DATE',
            'f': 'DATETIME',
            'w': 'VARCHAR(15)'
            }

def getSqlType(chType):
    if chType in sqlTypes:
        return sqlTypes[chType]
    else:
        return 'VARCHAR(30)'

def createArrayFromText(txt):
    if txt:
        return [fld.strip() for fld in txt.split(',')]
    else:
        return None

def createUnique(fldsArray):
    ftxt = '('
    if fldsArray:
        for el in fldsArray:
            ftxt += '%s, ' % el
        return ftxt[:-2] + ')'
    else:
        return None
    
class tbl():
    """
    INPUT PARAMETERS:
        1.tname   : table name   (e.g. er)
        2.lbs     : label single (e.g. worker)
        3.lbp     : label plural (e.g. workers)
        4.repFlds : Fields representing table in form 'field1, field2 , ...' (e.g. 'epo, ono' )
        5.uni     : Unique fields in form 'field1, field2, ...'
    """
    labelSimple = {}
    labelPlural = {}
    uniqueFields = {}
    reprFields = {}
    tableNamesArray = []
    lastTableInserted = None
    fields = {}
    
    def add(self, tname, lbs, lbp, repFlds=None, uni=None):
        self.labelSimple[tname] = lbs
        self.labelPlural[tname] = lbp
        self.reprFields[tname] = createArrayFromText(repFlds)
        self.uniqueFields[tname] = createArrayFromText(uni)
        self.tableNamesArray.append(tname)
        self.lastTableInserted = tname
    
    def sql(self):
        txtSql = u''
        for table in self.tableNamesArray:
            txtSql += self.tableSql(table)
        return txtSql
    
    def _rfieldsArray(self, tname):
        if tname not in self.tableNamesArray:
            return []
        if tables.reprFields[tname]:
            return tables.reprFields[tname]
        else:
            return tables.fields[tname]

    
    def reprFieldSql(self, table, idv):
        txtSql = u"SELECT %s.id," % table
        if tables.reprFields[table]:
            repFields = tables.reprFields[table]
        else:
            repFields = tables.fields[table]
        for pfield in repFields:
            txtSql += u" %s.%s || ' ' ||" % (table, pfield.strip())
        txtSql = txtSql[:-9]
        txtSql += u'AS z%s' % table 
        txtSql += "\nFROM %s" % table
        txtSql += "\nWHERE id=%s" % idv
        return txtSql
                    
    def selectSqls(self, table):
        txtSql = u"SELECT %s.id," % table
        innerJoinSql = u''
        for field in self.fields[table]:
            fieldType = field[0]
            if fieldType in 'cz':
                parentTable = field[1:]
                if tables.reprFields[parentTable]:
                    parFields = tables.reprFields[parentTable].split(',')
                else:
                    parFields =tables.fields[parentTable]
                if parFields:
                    for pfield in parFields:
                        txtSql += u" %s.%s || ' ' ||" % (parentTable, pfield.strip())
                    txtSql = txtSql[:-9]
                    txtSql += u'AS %s,' % field 
                innerJoinSql += u'\nINNER JOIN %s ON %s.id=%s.%s' % (parentTable,parentTable,table,field)
            else:
                txtSql += " %s.%s," % (table, field)
        txtSql = txtSql[:-1]
        txtSql += "\nFROM %s" % table
        txtSql += innerJoinSql
        return txtSql
    
    def tableSql(self, table):
        txtSql = u''
        txtSql += u"CREATE TABLE IF NOT EXISTS %s (\n" % table
        txtSql += u"id INTEGER PRIMARY KEY,\n"
        for field in self.fields[table]:
            fieldType = field[0]
            if fieldType in 'cz':
                ftvalue = 'INTEGER NOT NULL REFERENCES %s(id)' % field[1:]
            else:
                ftvalue = getSqlType(fieldType)
                if not fields.isNull[field]:
                    ftvalue += ' NOT NULL'
            if fields.isUnique[field]:
                ftvalue += ' UNIQUE'
            txtSql += u"%s %s,\n" % (field,ftvalue)
        if tables.uniqueFields[table]:
            txtSql += "UNIQUE %s\n);\n" % createUnique(tables.uniqueFields[table])
        else:
            txtSql = txtSql[:-2]
            txtSql += "\n);\n"
        return txtSql
            
tables = tbl()

def getTableLabelPlural(tblName):
    if tblName in tables.tableNamesArray:
        return tables.labelPlural[tblName]
    else:
        return tblName
    
def getTableLabel(tblName):
    if tblName in tables.tableNamesArray:
        return tables.labelSimple[tblName]
    else:
        return tblName
        
class fld():
    labelSmall = {}
    labelBig = {}
    isUnique = {}
    isNull = {}
    fieldNamesArray = []
    def add(self, fname, lbs, lbl, isNull=False, isUnique=False):
        self.labelSmall[fname] = lbs
        self.labelBig[fname] = lbl
        self.isNull[fname] = isNull
        self.isUnique[fname] = isUnique
        
        if fname in self.fieldNamesArray:
            pass
        else:
            self.fieldNamesArray.append(fname)
            
        try :
            tables.fields[tables.lastTableInserted].append(fname)
        except KeyError:
            tables.fields[tables.lastTableInserted] = [fname]
     
    def addFK(self,fname, unique=False):
        tblName = fname[1:]
        self.labelSmall[fname] = tables.labelSimple[tblName]
        self.labelBig[fname] = tables.labelSimple[tblName]
        self.isNull[fname]=False
        self.isUnique[fname]=unique 
        
        if fname in self.fieldNamesArray:
            pass
        else:
            self.fieldNamesArray.append(fname)
            
        try:
            tables.fields[tables.lastTableInserted].append(fname)
        except KeyError:
            tables.fields[tables.lastTableInserted] = [fname]   
fields = fld()

class defaultData():
    data = []
    def add(self,table,dataArray):
        self.data.append([table,dataArray])
    def sql(self):
        if len(self.data) == 0:
            return ''
        tstSql = u''
        sq1 = "INSERT INTO %s VALUES(" 
        for line in self.data:
            table = line[0]
            indata = line[1]
            if table not in tables.tableNamesArray:
                print("defaultData Error in table name %s" % table)
                return ''
            if len(indata) <> len(tables.fields[table])+1:
                print("defaultData Error .Number of fields (%s) not the same with number of fields (%s) of table %s" % (len(indata), len(tables.fields[table])+1,table))
                return ''
            tstSql += sq1 % table
            for el in indata:
                tstSql += "'%s'," % el
            tstSql = tstSql[:-1]
            tstSql += ");\n"
        return tstSql
ddata = defaultData()

def startSql():
    return 'BEGIN TRANSACTION;\n' + tables.sql() + ddata.sql() + 'COMMIT;'

def fillTreeMenu():
    mitems = []
    for table in tables.tableNamesArray:
        mitems.append([table,u'Πίνακες',tables.labelPlural[table],'tbl'])
        if table[:-1] in tables.tableNamesArray:
            mitems.append([table,u'ΠίνακεςMD',tables.labelPlural[table] + u'(md)','tblmd'])
    return mitems

strSep = "|| ' ' || "
lstrSep = len(strSep)

def recFields(fld):
    finalFields = u''
    if fld[0] not in 'cz':
        return fld
    else:
        ftable = fld[1:]
        repFields = tables._rfieldsArray(ftable)  
        for field in repFields:
            ap = recFields(field)
            if '.' in ap:
                val = ap
            else:
                val = '%s.%s %s' % (ftable, recFields(field),strSep)
            finalFields += val
    return finalFields

def recFieldsIJ(fld):
    ij = "\nINNER JOIN %s ON %s.id=%s.%s"
    if fld[0] not in 'cz':
        return ''
    else:
        ftable = fld[1:]
        repFields = tables._rfieldsArray(ftable)  
        for field in repFields:
            if field[0] in 'cz':
                if recFieldsIJ(field):
                    return ij % (field[1:],field[1:], ftable,field) +  recFieldsIJ(field)
                else:
                    return ij % (field[1:],field[1:], ftable,field)

def tblFlds(tname):
    if tname not in tables.tableNamesArray:
        return None
    sel = u"SELECT %s.id," % tname
    ij = u"\nINNER JOIN %s ON %s.id=%s.%s"
    ijf = u""
    ijt = u""
    for field in tables.fields[tname]:
        if field[0] in 'cz':
            ijf += ij % (field[1:],field[1:],tname,field)
            tijt = recFieldsIJ(field)
            if tijt:
                ijt += tijt
            sel += '%sAS %s,' % (recFields(field)[:-lstrSep], field)
            
        else:
            sel += '%s.%s,' % (tname,field)
    sel = sel[:-1]
    sel += "\nFROM %s" % tname
    sel += ijf
    sel += ijt
    #sel += '\nORDER BY %s.id' % tname
    return sel

def reprFlds(tname, idNo=None):
    if tname not in tables.tableNamesArray:
        if idNo:
            return 'SELECT * FROM %s WHERE id=%s' % (tname, idNo)
        else:
            return 'SELECT * FROM %s' % tname
    sel = u"SELECT %s.id," % tname
    ij = u"\nINNER JOIN %s ON %s.id=%s.%s"
    ijf = u""
    ijt = u""
    for field in tables._rfieldsArray(tname):
        if field[0] in 'cz':
            ijf += ij % (field[1:],field[1:],tname,field)
            tijt = recFieldsIJ(field)
            if tijt:
                ijt += tijt
            sel += '%s' % recFields(field)
            
        else:
            sel += '%s.%s %s' % (tname,field, strSep)

    sel = sel[:-1]
    sel = sel[:-lstrSep]
    sel += ' AS z%s' % tname
    sel += "\nFROM %s" % tname
    sel += ijf
    sel += ijt
    if idNo:
        sel += "\nWHERE %s.id=%s" % (tname,idNo)
    sel += '\nORDER BY %s.id' % tname
    return sel

def getLabel(fieldName):
    if fieldName in fields.fieldNamesArray:
        return fields.labelSmall[fieldName]
    elif fieldName == 'id':
        return u'ΑΑ'
    else:
        return fieldName
       
def getLabels(fieldNames):
    tmp = []
    for fieldName in fieldNames:
        tmp.append(getLabel(fieldName))
    return tmp

if __name__ == '__main__':
    tables.add('tst','Testing','Testing Fields','nfld, tfld', 'zfld, sfld')
    fields.add('bfld','Boolean','_')
    fields.add('ifld','Integer','_')
    fields.add('sfld','String','_')
    fields.add('jfld','StringNumeric','_')
    fields.add('nfld','Decimal','_')
    fields.add('tfld','Text','_')
    fields.add('zfld','FKey','_')
    tables.add('fld', 'sdfsdf','sdsdf',"ped1, ped2")
    fields.add('cfld','FKeyCombo','_')
    fields.add('dfld','Date','_')
    fields.add('efld','DateOrNull','_')
    fields.add('ffld','DateTime','_')
    fields.add('wfld','Special1','_')
    print(startSql())
    print(tables.reprFieldSql('tst',1))
    print(reprFlds('tst'))


