from PyQt5 import QtCore as qc
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
ARIGHT = qc.Qt.AlignRight | qc.Qt.AlignTrailing | qc.Qt.AlignVCenter
ALEFT = qc.Qt.AlignLeft | qc.Qt.AlignVCenter


class ModelTable(qc.QAbstractTableModel):
    def __init__(self, head_data):
        super().__init__()
        self.mdata = head_data['mdata']
        self.headers = head_data['headers']
        self.types = head_data['types']

    def rowCount(self, idx):
        return len(self.mdata)

    def columnCount(self, idx):
        return len(self.headers)

    def data(self, idx, role):
        if role == qc.Qt.DisplayRole:
            return self.mdata[idx.row()][idx.column()]
        # elif role == qc.Qt.BackgroundRole:
        #     return qg.QBrush(qc.Qt.red)
        # elif role == qc.Qt.CheckStateRole:
        #     return qc.Qt.Checked
        elif role == qc.Qt.FontRole:
            fnt = qg.QFont()
            fnt.setBold(True)
            return fnt
        elif role == qc.Qt.TextAlignmentRole:
            if self.types[idx.column()] == 0:
                return ALEFT
            elif self.types[idx.column()] == 1:
                return ARIGHT
            else:
                return ALEFT
        return qc.QVariant()

    def flags(self, idx):
        default_flags = qc.QAbstractItemModel.flags(self, idx)
        return qc.Qt.ItemIsEditable | default_flags

    def headerData(self, section, orientation, role):
        if role == qc.Qt.DisplayRole:
            if orientation == qc.Qt.Horizontal:
                return self.headers[section]
            elif orientation == qc.Qt.Vertical:
                return '%s' % (section + 1)
        return qc.QVariant()

    def setData(self, idx, value, role):
        if role == qc.Qt.EditRole:
            if idx.column() == 0:
                return False
            self.mdata[idx.row()][idx.column()] = value
        return True


if __name__ == '__main__':
    hdata = {'headers': ('id', 'epo'),
             'types': (0, 0),
             'mdata': [[1, 'ted'], [2, 'popi']]}
    import sys
    app = qw.QApplication(sys.argv)
    tview = qw.QTableView()
    tview.setModel(ModelTable(hdata))
    tview.show()
    sys.exit(app.exec_())
