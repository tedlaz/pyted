# from collections import namedtuple
from PyQt5 import QtCore as qc
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
# LMT = namedtuple('LMT', 'lmo metafora esoda ejoda')
ALIR = qc.Qt.AlignRight | qc.Qt.AlignTrailing | qc.Qt.AlignVCenter
STYLE_NORMAL = "background-color: rgb(200, 200, 200);"
STYLE_HILIGHTED = "background-color: rgb(200, 230, 200);"
STR_ACCOUNT = 'Λογαριασμός'
STR_TRANSFER = 'Μεταφορά'
STR_INCOME = 'Έσοδα'
STR_EXPENSE = 'Έξοδα'
STR_REST = 'Υπόλοιπο'
STR_TOTALS = 'Σύνολα'


class AccountWidget(qw.QWidget):
    acc_clicked = qc.pyqtSignal(str)

    def __init__(self, lmos, metafora, esoda, ejoda, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLE_NORMAL)
        self.setMouseTracking(True)
        self._create_ui()
        self.set_vals(lmos, metafora, esoda, ejoda)

    def _create_bold_font(self):
        font = qg.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        return font

    def set_vals(self, lmos, meta, eso, ejo):
        self.lmos = lmos
        self.meta = meta or 0
        self.eso = eso or 0
        self.ejo = ejo or 0
        self.logariasmos.setText(lmos)
        self.metafora.setText('%12.2f' % meta)
        self.esoda.setText('%12.2f' % eso)
        self.ejoda.setText('%12.2f' % (0 - ejo))
        ypo = meta + eso - ejo
        self.ypoloipo.setText('%12.2f' % ypo)

    def vals(self):
        return (self.lmos, self.meta, self.eso, self.ejo)

    def mousePressEvent(self, ev):
        qw.QMessageBox.information(self, 'Title Ted', 'lmos: %s' % self.lmos)
        self.acc_clicked.emit(self.lmos)
        return qw.QWidget.mousePressEvent(self, ev)

    def enterEvent(self, ev):
        self.setStyleSheet(STYLE_HILIGHTED)
        return qw.QWidget.enterEvent(self, ev)

    def leaveEvent(self, ev):
        self.setStyleSheet(STYLE_NORMAL)
        return qw.QWidget.leaveEvent(self, ev)

    def _create_ui(self):
        mainlayout = qw.QVBoxLayout(self)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        self.logariasmos = qw.QLabel(STR_ACCOUNT)
        self.logariasmos.setFont(self._create_bold_font())
        mainlayout.addWidget(self.logariasmos)
        layout = qw.QFormLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(1)
        mainlayout.addLayout(layout)
        lmetafora = qw.QLabel(STR_TRANSFER)
        lesoda = qw.QLabel(STR_INCOME)
        lejoda = qw.QLabel(STR_EXPENSE)
        lypoloipo = qw.QLabel(STR_REST)
        line = qw.QFrame()
        line.setFrameShadow(qw.QFrame.Plain)
        line.setLineWidth(3)
        line.setFrameShape(qw.QFrame.HLine)
        self.metafora = qw.QLabel('0,00')
        self.esoda = qw.QLabel('0,00')
        self.ejoda = qw.QLabel('0,00')
        self.ypoloipo = qw.QLabel('0,00')
        # alignement
        self.logariasmos.setAlignment(qc.Qt.AlignCenter)
        self.metafora.setAlignment(ALIR)
        self.esoda.setAlignment(ALIR)
        self.ejoda.setAlignment(ALIR)
        self.ypoloipo.setAlignment(ALIR)
        # add to layout manager
        layout.setWidget(0, qw.QFormLayout.LabelRole, lmetafora)
        layout.setWidget(0, qw.QFormLayout.FieldRole, self.metafora)
        layout.setWidget(1, qw.QFormLayout.LabelRole, lesoda)
        layout.setWidget(1, qw.QFormLayout.FieldRole, self.esoda)
        layout.setWidget(2, qw.QFormLayout.LabelRole, lejoda)
        layout.setWidget(2, qw.QFormLayout.FieldRole, self.ejoda)
        layout.setWidget(3, qw.QFormLayout.FieldRole, line)
        layout.setWidget(4, qw.QFormLayout.LabelRole, lypoloipo)
        layout.setWidget(4, qw.QFormLayout.FieldRole, self.ypoloipo)


class SideBar(qw.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        laym = qw.QVBoxLayout(self)
        scroll = qw.QScrollArea(self)
        scroll.setWidgetResizable(True)
        laym.addWidget(scroll)
        scont = qw.QWidget()
        lay = qw.QVBoxLayout(scont)
        self.layn = qw.QVBoxLayout()
        lay.addLayout(self.layn)
        self.totals = AccountWidget(STR_TOTALS, 0, 0, 0)
        lay.addWidget(self.totals)
        spacer = qw.QSpacerItem(20, 20, qw.QSizePolicy.Minimum,
                                qw.QSizePolicy.Expanding)
        lay.addItem(spacer)
        scroll.setWidget(scont)
        self.accounts = {}

    def add(self, lmos, met, eso, ejo):
        tlmos, tmet, teso, tejo = self.totals.vals()
        tmet += met
        teso += eso
        tejo += ejo
        if lmos in self.accounts:
            self.accounts[lmos].set_vals(lmos, met, eso, ejo)
        else:
            self.accounts[lmos] = AccountWidget(lmos, met, eso, ejo, self)
            self.layn.addWidget(self.accounts[lmos])
        self.totals.set_vals(tlmos, tmet, teso, tejo)

    def add_many(self, lmoi):
        '''lmoi: tuple'''
        lmoi.sort()
        for lmo in lmoi:
            self.add(*lmo)


def test_sidebar(lmoi):
    import sys
    app = qw.QApplication(sys.argv)
    sbar = SideBar()
    sbar.add_many(lmoi)
    sbar.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    lms = [('ταμείο.μετρητά.τσέπη', 52699.41, 11649.91, 64036.22),
           ('ταμείο.τράπεζες.visa', 4324.38, -1260.13, 3075.25),
           ('ταμείο.μετρητά.σπίτι', 32256.85, 4513.91, 16770.76),
           ('ταμείο.τράπεζες.alpha', 34954.91, 3804.31, 31205.82),
           ('ταμείο.τράπεζες.αττικής', -14900, 26040.22, 11136.62)
           ]
    test_sidebar(lms)
