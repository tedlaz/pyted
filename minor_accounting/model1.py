from PyQt5 import QtCore as qc
from PyQt5 import QtWidgets as qw
# from PyQt5 import QtGui as qg
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
            # if idx.column() == 0:
            #     yyyy, mm, dd = self.mdata[idx.row()][idx.column()].split('-')
            #     return qc.QDate(int(yyyy), int(mm), int(dd))
            return self.mdata[idx.row()][idx.column()]
        # elif role == qc.Qt.BackgroundRole:
        #     return qg.QBrush(qc.Qt.red)
        # elif role == qc.Qt.CheckStateRole:
        #     return qc.Qt.Checked
        # elif role == qc.Qt.FontRole:
        #     fnt = qg.QFont()
        #     fnt.setBold(True)
        #     return fnt
        elif role == qc.Qt.EditRole:
            return self.mdata[idx.row()][idx.column()]
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
            self.mdata[idx.row()][idx.column()] = value
        self.dataChanged.emit(idx, idx, [])
        return True


class Form1(qw.QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.model = ModelTable(data)
        lay = qw.QVBoxLayout(self)
        self.tview = qw.QTableView()
        self.tview.setModel(self.model)
        lay.addWidget(self.tview)
        self.map = qw.QDataWidgetMapper(self)
        self.map.setModel(self.model)
        self.map.setSubmitPolicy(qw.QDataWidgetMapper.ManualSubmit)
        self.text = qw.QLineEdit()
        self.map.addMapping(self.text, 4)
        lay.addWidget(self.text)
        self.tApo = qc.QStringListModel(('ταμείο', 'τράπεζα'), self)
        typeComboBox = qw.QComboBox()
        typeComboBox.setModel(self.tApo)
        # self.map.addMapping(typeComboBox, 1, b'currentIndex')
        self.map.addMapping(typeComboBox, 1)
        lay.addWidget(typeComboBox)
        dat = qw.QDateEdit()
        dat.setCalendarPopup(True)
        lay.addWidget(dat)
        self.map.addMapping(dat, 0)
        self.btn = qw.QPushButton('save')
        lay.addWidget(self.btn)
        self.btn.clicked.connect(self.map.submit)
        self.tview.clicked.connect(self.map.setCurrentModelIndex)
        self.map.toFirst()


if __name__ == '__main__':
    hdata = {'headers': ('Ημ/νία', 'Από', 'Σε', 'Ποσό', 'Σχόλια'),
             'types': (0, 0, 0, 1, 0),
             'mdata': [['2018-10-15', '0', 'εξοδα', 10, 'Δοκιμή'],
                       ['2018-01-02', '1', 'εξοδα', 23, 'Δεύτερη']
                       ]}
    import sys
    app = qw.QApplication(sys.argv)
    form = Form1(hdata)
    form.show()
    sys.exit(app.exec_())
