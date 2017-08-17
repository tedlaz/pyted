'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''
from PyQt5 import QtGui as Qg
from PyQt5 import QtCore as Qc
from PyQt5 import QtWidgets as Qw


LABEL, VAL, QT = range(3)


class FormTemplate(Qw.QDialog):
    '''Απλή φόρμα για δοκιμή
    '''
    def __init__(self, data, parent=None):
        '''
        :param data: Dictionary with data values
                     {'field': ['label', value or None, etc]}
        :param dbf: Database file path
        :param did: The id of the record. None for new record.
        :param idon: If True id is visible in form
        '''
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Form template')
        # basic data here
        self.data = data
        # Set main layout
        self.mainlayout = Qw.QVBoxLayout()
        self.setLayout(self.mainlayout)
        # Create widgets here and add them to formlayout
        self._create_and_fill_fields()
        self._create_buttons()

    def _create_and_fill_fields(self):
        flayout = Qw.QFormLayout()
        self.mainlayout.addLayout(flayout)
        self.widgets = {}
        # Add fields to form
        for i, fld in enumerate(self.data):
            if fld == 'id':
                continue
            self.widgets[fld] = Qw.QLineEdit()
            if self.data[fld][VAL]:  # if not None or empty string
                self.widgets[fld].setText('%s' % self.data[fld][VAL])
            # replace possible None with empty string for correct comparisson
            else:
                self.data[fld][VAL] = ''
            flayout.insertRow(i, Qw.QLabel(self.data[fld][LABEL]),
                              self.widgets[fld])

    def _create_buttons(self):
        '''Create buttons for the form'''
        # Create layout first
        buttonlayout = Qw.QHBoxLayout()
        self.mainlayout.addLayout(buttonlayout)
        # Create buttons here
        self.bcancel = Qw.QPushButton(u'Ακύρωση', self)
        self.bsave = Qw.QPushButton(u'Αποθήκευση', self)
        # Add them to buttonlayout
        buttonlayout.addWidget(self.bcancel)
        buttonlayout.addWidget(self.bsave)
        # Make connections here
        self.bcancel.clicked.connect(self.close)
        self.bsave.clicked.connect(self.save)

    def validate(self):
        return False

    def save(self):
        print(self.get_data_from_form(False))

    def get_data_from_form(self, only_changed=False):
        '''Get data from the form. Assume id already exists.
        '''
        dtmp = {'id': self.data['id'][VAL]}
        for field in self.widgets:
            if only_changed:
                if self.data[field][VAL] != self.widgets[field].text():
                    dtmp[field] = self.widgets[field].text()
            else:
                dtmp[field] = self.widgets[field].text()
        return dtmp

    def is_dirty(self):
        '''Check if any value changed by user'''
        startv = {}
        for field in self.data:
            startv[field] = self.data[field][VAL]
        if startv == self.get_data_from_form():
            return False
        else:
            return True


if __name__ == '__main__':
    import sys
    app = Qw.QApplication([])
    dialog = FormTemplate({'id': ['αα', 1],
                           'epo': ['Επώνυμο', None],
                           'ono': ['Όνομα', ''],
                           'pat': ['Πατρώνυμο', ''],
                           'mit': ['Μητρώνυμο', '']
                           })
    dialog.show()
    appex = app.exec_()
    sys.exit(appex)
