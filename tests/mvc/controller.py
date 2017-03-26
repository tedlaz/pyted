# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
import model_table_sqlite as model_table
import view_grid

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    model1 = model_table.ModelTable('m.m13', 'm12_fpr')
    viewgrid1 = view_grid.ViewGrid(model1)
    viewgrid1.show()
    # model2 = model_table.ModelTable('el2015.sql3', 'tr')
    # viewgrid2 = view_grid.ViewGrid(model2)
    # viewgrid2.show()
    sys.exit(app.exec_())
