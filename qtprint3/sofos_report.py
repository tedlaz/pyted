import yaml
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import report_table as tr
from sofos import qt


def open_yaml(filename):
    data = None
    with open(filename) as ofile:
        data = yaml.load(ofile.read())
    return data


class testprn1(Qw.QDialog):
    def __init__(self, f, dfi):
        Qw.QDialog.__init__(self)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.rep = tr.TableReport(f, dfi)
        tstButton = Qw.QPushButton('test')
        tstButton.clicked.connect(self.onClick)
        main_layout = Qw.QVBoxLayout()
        form_layout = Qw.QFormLayout()
        main_layout.addLayout(form_layout)
        lbl1, date1 = Qw.QLabel('test'), qt.TDate()
        form_layout.insertRow(0, lbl1, date1)
        layout = Qw.QHBoxLayout()
        main_layout.addLayout(layout)
        layout.addWidget(tstButton)
        self.setLayout(main_layout)

    def onClick(self):
        self.rep.printPreview()
        # self.accept()


if __name__ == '__main__':
    import sys
    yfile = '/home/ted/prj/pyted/qtprint3/tst.yml'
    adic = open_yaml(yfile)
    dfi = [['Λάζαρος Θεόδωρος', 2, 100, 10, 20, 30, 0, 0, 10, 90],
           ['Δαζέα Καλλιόπη', 5, 150, 15, 30, 45, 0, 0, 15, 135],
           ['Δαζέας Νικόλαος', 5, 150, 15, 30, 45, 0, 0, 15, 135],
           ]
    app = Qw.QApplication(sys.argv)
    window = testprn1(adic, dfi * 60)
    window.show()
    sys.exit(app.exec_())
