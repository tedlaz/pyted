# -*- coding: utf-8 -*-


from PyQt4 import QtGui


class Treeitem(QtGui.QTreeWidgetItem):

    def __init__(self, dicval, parent):  # {'name': 'test', 'title': u'Δοκ'}
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.name = dicval.get('name', 'No Name')
        self.type = dicval.get('typ', 'No Type')
        self.setText(0, dicval.get('title', 'No Title'))


class Treemenu(QtGui.QTreeWidget):

    def __init__(self, vals, parent=None):
        QtGui.QTreeWidget.__init__(self, parent)
        self.headerItem().setText(0, u'Μενου')
        it_tables = QtGui.QTreeWidgetItem(self)
        self.topLevelItem(0).setText(0, u"Πίνακες")
        for i, el in enumerate(vals):
            it0 = Treeitem(el, it_tables)
        self.doubleClicked.connect(self.show1)

    def show1(self):
        typos = self.currentItem().type
        if typos == 'tbl':
            print('This is table')
        else:
            print('Not a table')
        print(self.currentItem().name)


if __name__ == '__main__':
    from sys import argv, exit
    vals = [{'name': 'erg', 'title': u'Εργαζόμενος', 'typ': 'tbl'},
            {'name': 'er2', 'title': u'Σκατά', 'typ': 'nbl'}]
    app = QtGui.QApplication(argv)

    form = Treemenu(vals)
    form.show()
    s = app.exec_()
    exit(s)
