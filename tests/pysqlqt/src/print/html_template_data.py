# *- coding: utf-8 -*
from PyQt4 import QtGui, Qt

header = u'''\
<!doctype html>
<html>
<head>
   <meta charset="UTF-8">
</head>
<body>
'''
footer = "</body>\n</html>"
page_break = "<p style='page-break-before:always;'>\n"


def render_data_to_html(list_of_dict, html_template):
    '''
    Create html file from html template and data
    array_of_dict : List of dictionaries
    html_template : Html text containing formatting tags
    '''
    array_len = len(list_of_dict)
    assert array_len > 0
    # assert isinstance(html_template, str)
    final_html = header
    html_temp = html_template  # .decode('utf-8')
    for i, dic in enumerate(list_of_dict):
        try:
            final_html += html_temp.format(**dic)
            if i == (array_len - 1):
                final_html += footer
            else:
                final_html += page_break
        except KeyError as ke:
            msg = "Error in array line %s. There is not key %s in %s"
            print msg % (i, ke, dic)
            return ''
    return final_html  # .encode('utf-8')


def render_data_to_html_from_file(list_of_dict, file_html_template):
    html_temp = u''
    with open(file_html_template) as afile:
        html_temp = afile.read()
    html_temp = u'%s' % html_temp.decode('utf-8')
    return render_data_to_html(list_of_dict, html_temp)


class Test(QtGui.QDialog):
    def __init__(self, html, parent=None):
        super(Test, self).__init__(parent)
        self.html = html
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.text = QtGui.QTextEdit(self)
        self.text.setHtml(html)
        tstButton = QtGui.QPushButton('preview')
        tstButton.clicked.connect(self.preview)
        htmlButton = QtGui.QPushButton('Export to html file')
        htmlButton.clicked.connect(self.export_to_html)
        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(htmlButton)
        hlayout.addWidget(tstButton)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.text)
        layout.addLayout(hlayout)
        self.setLayout(layout)

    def preview(self):
        dialog = QtGui.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.text.print_)
        dialog.exec_()

    def export_to_html(self):
        fname = '%s' % QtGui.QFileDialog.getSaveFileName(
            self, u"%Αποθήκευση ως", 'test.html', u"Αρχείο (*.html)")
        with open(fname, 'w') as afile:
            afile.write(self.html.encode('utf-8'))


if __name__ == '__main__':
    import sys
    template_file = '../recources/templates/template1.html'
    arr = [{'name': u'Θεόδωρος', 'age': '52'},
           {'name': u'Πόπη', 'age': '40'}]
    html1 = render_data_to_html_from_file(arr, template_file)
    print html1
    app = QtGui.QApplication(sys.argv)
    window = Test(html1)
    window.show()
    app.exec_()
