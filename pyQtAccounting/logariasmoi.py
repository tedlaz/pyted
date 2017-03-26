# -*- coding: utf-8 -*-
import sqlite3
import decimal


#######################################################################
#  Utility Functions
#######################################################################

def isNum(value): # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters : 
            1.value : the value to check against.
        output: True or False
    """
    try: float(value)
    except ValueError: return False
    else: return True

def dec(poso , dekadika=2 ):
    """ 
    use : Given a number, it returns a decimal with a specific number of decimal digits
    input Parameters:
          1.poso     : The number for conversion in any format (e.g. string or int ..)
          2.dekadika : The number of decimals (default 2)
    output: A decimal number     
    """
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)
    
class account():
    '''
    General Ledger account 
    '''
    def __init__(self,db=None):
        self.kodikos     = None
        self.logariasmos = None
        self.perigrafi   = None
        self.db          = db
    def getFromDB(self,kodikos=None,logariasmos=None,perigrafi=None):
        if self.db:
            if kodikos:
                return 'Kodikos'
            elif logariasmos:
                return 'Logariasmos'
            elif perigrafi:
                return 'Perigrafi'
            else:
                pass
        else:
            return None

    def new(self,_log,_per):
        self.logariasmos = _log
        self.perigrafi   = _per
    def isValid(self):
        if (self.kodikos and self.logariasmos and self.perigrafi):
            return True
        else :
            return False
        
class transaction_line():
    '''
    General ledger transaction line
    '''
    def __init__(self):
        self.id      = None
        self.tran_id = None
        self.lmos_id = None
        self.per2    = None
        self.xr      = None
        self.pi      = None        
class transaction():
    '''
    General ledger transaction (Body and Lines) 
    '''
    def __init__(self):
        self.no    = None
        self.imnia = None
        self.par   = None
        self.per   = None
        self.lines = []
        
if __name__ == "__main__":
    acc = account('tst')
    acc.kodikos = '1'
    acc.logariasmos = '38.00.0000'
    acc.perigrafi = 'This is test'
    print acc.isValid()
    print acc.getFromDB(logariasmos='teddy')
    
