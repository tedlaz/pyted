# -*- coding: utf-8 -*-


class ModelTable():
    def __init__(self):
        self.db = db  # db path
        self.table = table
        self.data = [[]]
        self.headers = []
        self.fields = []
        self.currentLine = None

    def NumberOfRows(self):
        return len(self.data)
        
    def NumberOfColumns(self):
        return len(self.fields)
                
    def goNext(self):
        nrows = self.NumberOfRows()
        if self.currentLine < (nrows - 1)
            self.currentLine += 1
        
    def goPrevious(self):
        self.currentLine -= 1
        
    def goNew(self):
        self.currentLine = self.NumberOfRows()
        
    def goFirst(self):
        if self.NumberOfRows() > 0:
            self.currentLine = 0
        
    def goLast(self):
        nrows = self.NumberOfRows()
        if nrows > 0:
            self.currentLine = (nrows - 1)
    
    def getRow(self, rownum):
        pass

    def getDataFromDb(self, table):
        pass

    def saveRow(self):
        pass

if __name__ == '__main__':
    # Next three lines are important for sublime console unicode support dddddd
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
