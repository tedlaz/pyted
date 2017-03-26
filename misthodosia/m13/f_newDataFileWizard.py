# -*- coding: utf-8 -*-
'''
Created on 15 Φεβ 2013

@author: tedlaz
'''
sqlco = u"INSERT INTO  m12_co  VALUES (1,'{0}','{1}','{2}',{3},'{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')"
from PyQt4 import QtCore, QtGui,Qt   
from utils import  dbutils,widgets
from osyk import osyk
from utils.qtutils import fFindFromList
import datetime

class NewDbWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(NewDbWizard, self).__init__(parent)
        #self.setAttribute(Qt.Qt.WA_DeleteOnClose) Οχι γιατί δημιουργείται πρόβλημα ...
        #self.addPage(IntroPage())
        self.addPage(coDataPage())
        self.addPage(coDataPage2())
        self.addPage(filePage())
        self.addPage(finalPage())
        
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setOption(QtGui.QWizard.IndependentPages,True)
        
        #self.setPixmap(QtGui.QWizard.BannerPixmap,QtGui.QPixmap(':/banner'))
        #self.setPixmap(QtGui.QWizard.BackgroundPixmap, QtGui.QPixmap(':/background'))

        self.setWindowTitle(u"Οδηγός Δημιουργίας Νέου Αρχείου Μισθοδοσίας")

    def accept(self):
        #print '%s %s %s' % (self.field('epon'),self.field('cotyp_id'),self.field('fname'))
        fileSql = open('newDb.sql')
        script = u''
        for lines in fileSql:
            script += u'%s' % lines.decode('utf-8')
        dbutils.executeScript(script, self.field('fname'))
        sqlCo = sqlco.format(self.field('epon'),self.field('onom'),self.field('patr'),self.field('cotyp_id'),
                             self.field('ame'),self.field('afm'),self.field('doy'),self.field('dra'),
                             self.field('pol'),self.field('odo'),self.field('num'),self.field('tk'),
                             self.field('ikac'),self.field('ikap'))
        #print sqlCo
        dbutils.commitToDb(sqlCo, self.field('fname'))
        sqlCoy = u"INSERT INTO m12_coy VALUES (1,1,'Κεντρικό','%s')" % self.field('kad')
        dbutils.commitToDb(sqlCoy, self.field('fname'))
        
        etos = datetime.datetime.now().year
        dbutils.commitToDb(u"INSERT INTO m12_xrisi (xrisi,xrisip) VALUES ('{0}','Χρήση {0}')".format(etos), self.field('fname'))
        
        eidList = osyk.eid_cad_listFilteredDouble(self.field('kad'))
        print eidList
        sqleid_ = u"INSERT INTO m12_eid (eidp,keid) VALUES ('{0}','{1}');\n"
        sqleid = u''
        for el in eidList:
            sqleid += sqleid_.format(el[1],el[0])
        dbutils.executeScript(sqleid,self.field('fname'))
        super(NewDbWizard, self).accept()

class IntroPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(u"Οδηγίες")
        #self.setPixmap(QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(':/watermark1'))

        label = QtGui.QLabel(u"Αυτός ο οδηγός θα δημιουργήσει νέο Αρχείο Μισθοδοσίας.\n\n "
                u"Εσείς θα πρέπει απλά να εισάγετε τις απαραίτητες παραμέτρους "
                u"καθώς και το όνομα του αρχείου και το σημείο αποθήκευσης.\n\n"
                u"Μπορείτε σε κάθε βήμα να αναθεωρήσετε και να επιστρέψετε.\n\n"
                u"Πατήστε δημιουργία στην τελευταία οθόνη για να ολοκληρώσετε.")
        label.setWordWrap(True)
               
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        
        self.setLayout(layout)

class coDataPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(coDataPage, self).__init__(parent)
        #parent.button(QtGui.QWizard.BackButton).setVisible(False)
        #self.buttonText(QtGui.QWizard.NextButton)
        self.setButtonText(QtGui.QWizard.BackButton,u'< Πίσω')
        self.setButtonText(QtGui.QWizard.NextButton,u'Επόμενο >')
        self.setButtonText(QtGui.QWizard.CancelButton,u'Ακύρωση')
        
        self.setTitle(u"Πληροφορίες εταιρίας")
        self.setSubTitle(u"Συμπληρώστε τα βασικά στοιχεία της εταιρίας")
        #self.setPixmap(QtGui.QWizard.LogoPixmap, QtGui.QPixmap(':/logo1'))
        
        cotypLabel = QtGui.QLabel(u"Τύπος επιχείρησης:")
        cotyp = widgets.DbComboBox([[1,u'Νομικό Πρόσωπο'],[2,u'Φυσικό Πρόσωπο']])
        cotypLabel.setBuddy(cotyp)
        
        
        eponNameLabel = QtGui.QLabel(u"Επωνυμία:")
        eponNameLineEdit = QtGui.QLineEdit()
        eponNameLabel.setBuddy(eponNameLineEdit)

        onomLabel = QtGui.QLabel(u"Όνομα (Για φυσικά πρόσωπα):")
        onomLineEdit = QtGui.QLineEdit()
        onomLineEdit.setDisabled(True)
        onomLabel.setBuddy(onomLineEdit)
        
        patrLabel = QtGui.QLabel(u"Πατρώνυμο (Για φυσικά πρόσωπα):")
        patrLineEdit = QtGui.QLineEdit()
        patrLineEdit.setDisabled(True)
        patrLabel.setBuddy(patrLineEdit)
        
        def onCotypActivated():
            if cotyp.currentIndex() ==1:
                onomLineEdit.setDisabled(False)
                patrLineEdit.setDisabled(False)
            else:
                onomLineEdit.setText('')
                patrLineEdit.setText('')
                onomLineEdit.setDisabled(True)
                patrLineEdit.setDisabled(True)               
            
        cotyp.activated.connect(onCotypActivated)
        
        kadLabel = QtGui.QLabel(u"Κωδικός αρ.Δραστηριότητας:")
        kadLineEdit = QtGui.QLineEdit()
        kadLabel.setBuddy(kadLineEdit)
        kadLineEdit.setReadOnly(True)
                         
        kadFindButton = QtGui.QPushButton(u'Εύρεση ΚΑΔ')
        
        kadLayout = QtGui.QHBoxLayout()
        kadLayout.addWidget(kadLineEdit)
        kadLayout.addWidget(kadFindButton)
        
        kadpLabel = QtGui.QLabel(u"Περιγραφή αρ.Δραστηριότητας:")
        kadpTextEdit = QtGui.QTextEdit()
        kadpLabel.setBuddy(kadpTextEdit)
        kadpTextEdit.setReadOnly(True)

        draLabel = QtGui.QLabel(u"Συντομογραφία Δραστηριότητας:")
        draLineEdit = QtGui.QLineEdit()
        draLabel.setBuddy(draLineEdit)
                
        def openFindDlg():
            kadList = osyk.cad_list()
            head = [u'ΚΑΔ',u'Περιγραφή']
            cw   = [35,300]   
            form = fFindFromList(kadList,head,cw)
            if form.exec_() == QtGui.QDialog.Accepted:
                kadLineEdit.setText(form.array[0])
                kadpTextEdit.setText(form.array[1])
                 
        kadFindButton.clicked.connect(openFindDlg) 
                      
                      
        self.registerField('cotyp_id',cotyp,'timi')
        self.registerField('epon*', eponNameLineEdit)
        self.registerField('onom', onomLineEdit)
        self.registerField('patr', patrLineEdit)
        self.registerField('kad*', kadLineEdit)
        self.registerField('dra*', draLineEdit)
        #self.registerField('kadt*', kadpTextEdit)

        layout = QtGui.QGridLayout()
        layout.addWidget(cotypLabel, 0, 0)
        layout.addWidget(cotyp, 0, 1)
        layout.addWidget(eponNameLabel, 1, 0)
        layout.addWidget(eponNameLineEdit, 1, 1)
        layout.addWidget(onomLabel, 2, 0)
        layout.addWidget(onomLineEdit, 2, 1)
        layout.addWidget(patrLabel, 3, 0)
        layout.addWidget(patrLineEdit, 3, 1)
        layout.addWidget(kadLabel, 4, 0)
        layout.addLayout(kadLayout, 4, 1)
        layout.addWidget(kadpLabel,5, 0)
        layout.addWidget(kadpTextEdit, 5, 1,2,1)  
        layout.addWidget(draLabel,7, 0)
        layout.addWidget(draLineEdit,7, 1)
        
        self.setLayout(layout)
        
class coDataPage2(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(coDataPage2, self).__init__(parent)
        
        self.setButtonText(QtGui.QWizard.BackButton,u'< Πίσω')
        self.setButtonText(QtGui.QWizard.NextButton,u'Επόμενο >')
        self.setButtonText(QtGui.QWizard.CancelButton,u'Ακύρωση')
        
        self.setTitle(u"Πληροφορίες εταιρίας")
        self.setSubTitle(u"Συμπληρώστε τα υπόλοιπα στοιχεία της εταιρίας")

        afmLabel = QtGui.QLabel(u"ΑΦΜ:")
        afmLineEdit = QtGui.QLineEdit()
        afmLabel.setBuddy(afmLineEdit)

        doyLabel = QtGui.QLabel(u"ΔΟΥ:")
        doyLineEdit = QtGui.QLineEdit()
        doyLabel.setBuddy(doyLineEdit)
        doyLineEdit.setReadOnly(True)
        
        doyFindButton = QtGui.QPushButton(u'...')
        doyFindButton.setMaximumSize(QtCore.QSize(20, 50))
        doyLayout = QtGui.QHBoxLayout()
        doyLayout.addWidget(doyLineEdit)
        doyLayout.addWidget(doyFindButton)
        
        def openFindDlg():
            head = [u'Κωδ',u'ΔΟΥ']
            cw   = [35,300]   
            form = fFindFromList(osyk.doy_list('./osyk/doy.txt'),head,cw)
            if form.exec_() == QtGui.QDialog.Accepted:
                doyLineEdit.setText(form.array[1])
                
        doyFindButton.clicked.connect(openFindDlg)
         
        poliLabel = QtGui.QLabel(u"Πόλη:")
        poliLineEdit = QtGui.QLineEdit()
        poliLabel.setBuddy(poliLineEdit)
        
        tkLabel = QtGui.QLabel(u"Ταχ.Κωδικός:")
        tkLineEdit = QtGui.QLineEdit()
        tkLabel.setBuddy(tkLineEdit)        

        odosLabel = QtGui.QLabel(u"Οδός:")
        odosLineEdit = QtGui.QLineEdit()
        odosLabel.setBuddy(odosLineEdit)
        
        numLabel = QtGui.QLabel(u"Αριθμός:")
        numLineEdit = QtGui.QLineEdit()
        numLabel.setBuddy(numLineEdit) 

        ameLabel = QtGui.QLabel(u"Αρ.Μητρ.ΙΚΑ:")
        ameLineEdit = QtGui.QLineEdit()
        ameLabel.setBuddy(ameLineEdit)
        
        ikacLabel = QtGui.QLabel(u"Κωδ.ΙΚΑ:")
        ikacLineEdit = QtGui.QLineEdit()
        ikacLabel.setBuddy(ikacLineEdit)
        ikacLineEdit.setReadOnly(True)

        ikaLabel = QtGui.QLabel(u"Υπ/μα.ΙΚΑ:")
        ikaLineEdit = QtGui.QLineEdit()
        ikaLabel.setBuddy(ikaLineEdit)
        ikaLineEdit.setReadOnly(True)
                
        ikaFindButton = QtGui.QPushButton(u'...')
        ikaFindButton.setMaximumSize(QtCore.QSize(20, 50))
        
        ikaLayout = QtGui.QHBoxLayout()
        ikaLayout.addWidget(ikaLineEdit)
        ikaLayout.addWidget(ikaFindButton)
        
        def openFindDlgIKA():
            head = [u'Κωδ',u'Υποκατάστημα ΙΚΑ']
            cw   = [35,300]   
            form = fFindFromList(osyk.doy_list('./osyk/ika.txt'),head,cw)
            if form.exec_() == QtGui.QDialog.Accepted:
                ikacLineEdit.setText(form.array[0])
                ikaLineEdit.setText(form.array[1])
                
        ikaFindButton.clicked.connect(openFindDlgIKA)
        
        self.registerField('afm*',afmLineEdit)
        self.registerField('doy*',doyLineEdit)
        self.registerField('pol*',poliLineEdit)
        self.registerField('odo',odosLineEdit)
        self.registerField('num',numLineEdit)
        self.registerField('tk',tkLineEdit)
        self.registerField('ikac*',ikacLineEdit)
        self.registerField('ikap*',ikaLineEdit)
        self.registerField('ame*',ameLineEdit)
        
        layout = QtGui.QGridLayout()
        
        layout.addWidget(afmLabel, 0, 0)
        layout.addWidget(afmLineEdit, 0, 1)
        
        layout.addWidget(doyLabel, 0, 2)
        layout.addLayout(doyLayout, 0, 3)        

        layout.addWidget(poliLabel, 1, 0)
        layout.addWidget(poliLineEdit, 1, 1)

        layout.addWidget(tkLabel, 1, 2)
        layout.addWidget(tkLineEdit, 1, 3)
 
        layout.addWidget(odosLabel, 2, 0)
        layout.addWidget(odosLineEdit, 2, 1)

        layout.addWidget(numLabel, 2, 2)
        layout.addWidget(numLineEdit, 2, 3)

        layout.addWidget(ameLabel, 3, 0)
        layout.addWidget(ameLineEdit, 3, 1)
        
        layout.addWidget(ikacLabel, 4, 0)
        layout.addWidget(ikacLineEdit, 4, 1)

        layout.addWidget(ikaLabel, 4, 2)
        layout.addLayout(ikaLayout, 4, 3)                               
        self.setLayout(layout)                
                        
class filePage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(filePage, self).__init__(parent)

        self.setButtonText(QtGui.QWizard.BackButton,u'< Πίσω')
        self.setButtonText(QtGui.QWizard.NextButton,u'Επόμενο >')
        self.setButtonText(QtGui.QWizard.CancelButton,u'Ακύρωση')
        
        self.setTitle(u"Όνομα αρχείου")
        self.setSubTitle(u"Δώστε όνομα και περιοχή αποθήκευσης")
        #self.setPixmap(QtGui.QWizard.LogoPixmap, QtGui.QPixmap(':/logo1'))

        fileNameLabel = QtGui.QLabel(u"Όνομα αρχείου:")
        self.fileNameLineEdit = QtGui.QLineEdit()
        self.fileNameLineEdit.setReadOnly(True)
        fileNameLabel.setBuddy(self.fileNameLineEdit)
        
        butFile = QtGui.QPushButton(u'...')
        butFile.clicked.connect(self.fSave)
        
        fileLayout = QtGui.QHBoxLayout() 
        
        fileLayout.addWidget(self.fileNameLineEdit)
        fileLayout.addWidget(butFile)
        
        patrLabel = QtGui.QLabel(u"Πατρώνυμο (Για φυσικά πρόσωπα):")
        patrLineEdit = QtGui.QLineEdit()
        patrLabel.setBuddy(patrLineEdit)

        cotypLabel = QtGui.QLabel(u"Τύπος επιχείρησης:")
        cotyp = QtGui.QComboBox()
        cotypLabel.setBuddy(cotyp)
        cotyp.addItems([u'1.Νομικό Πρόσωπο',u'2.Φυσικό Πρόσωπο'])

        self.registerField('fname*', self.fileNameLineEdit)

        layout = QtGui.QGridLayout()
        layout.addWidget(fileNameLabel, 0, 0)
        layout.addLayout(fileLayout, 0, 1)
    
        self.setLayout(layout)
        
    def fSave(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                "QFileDialog.getSaveFileName()",
                self.field('fname'),
                "payroll m13 (*.m13)", QtGui.QFileDialog.Options())
        if fileName:
            self.fileNameLineEdit.setText(fileName)
    
class finalPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(finalPage, self).__init__(parent)
        
        self.setButtonText(QtGui.QWizard.BackButton,u'< Πίσω')
        self.setButtonText(QtGui.QWizard.FinishButton,u'Ολοκλήρωση')
        self.setButtonText(QtGui.QWizard.CancelButton,u'Ακύρωση')
        
        self.setTitle(u"Δημιουργία αρχείου ")
        #self.setPixmap(QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(':/watermark2'))

        self.label = QtGui.QLabel()
        self.label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initializePage(self):
        finishText = self.wizard().buttonText(QtGui.QWizard.FinishButton)
        finishText.replace('&', '')
        txt = u'Προσοχή , θα δημιουργηθεί αρχείο μισθοδοσίας με τις παρακάτω παραμέτρους :\n\n'
        txt += u'Στοιχεία Επιχείρησης : %s \n\n' % self.field('epon')
        txt += u'Όνομα Αρχείου : %s \n\n' % self.field('fname') 
        txt += u"\nΠατήστε %s για να ολοκληρωθεί η διαδικασία." % finishText
        self.label.setText(txt)

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = NewDbWizard()
    wizard.show()
    sys.exit(app.exec_())
