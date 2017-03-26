from PyQt5 import QtWidgets as qw


class Form(qw.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        nameLabel = qw.QLabel("Όνομα:")
        self.nameLine = qw.QLineEdit()
        self.submitButton = qw.QPushButton("Υποβολή")

        buttonLayout1 = qw.QVBoxLayout()
        buttonLayout1.addWidget(nameLabel)
        buttonLayout1.addWidget(self.nameLine)
        buttonLayout1.addWidget(self.submitButton)

        self.submitButton.clicked.connect(self.submitContact)

        mainLayout = qw.QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(buttonLayout1, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Γειά ..")

    def submitContact(self):
        name = self.nameLine.text()

        if name == "":
            qw.QMessageBox.information(self, "Empty Field",
                                    "Please enter a name and address.")
            qw.QMessageBox.critical(self, 'δσ', "Σκατά στο στόμα σου φίλε..")
            return
        else:
            qw.QMessageBox.information(self, "Επιτυχία!",
                                    "Καλώς ήρθες %s!" % name)
            qw.QMessageBox.critical(self, 'δσ', "Σκατά στο στόμα σου φίλε..")

if __name__ == '__main__':
    import sys

    app = qw.QApplication(sys.argv)

    screen = Form()
    screen.show()

    sys.exit(app.exec_())
