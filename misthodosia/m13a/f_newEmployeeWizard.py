# -*- coding: utf-8 -*-
'''
Created on 15 Φεβ 2013

@author: tedlaz
'''

from PyQt4 import QtCore, QtGui,Qt
from collections import OrderedDict
import  utils_db as dbutils
import widgets
from utils_qt import fFindFromList 
import osyk  
#import classwizard_rc
sqlInsertFpr = u'''
INSERT INTO m12_fpr (epon,onom,patr,mitr,sex_id,igen,afm,amka,aika,pol,odo,num,tk) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')
'''
sqlInsertPro = u'''
INSERT INTO m12_pro (prod,fpr_id,coy_id,eid_id,proy,aptyp_id,apod) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
'''
class NewEmpWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(NewEmpWizard, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        if parent:
            self.db = parent.parent.db
        else:
            self.db = None
        self.addPage(IntroPage(self))
        self.addPage(coDataPage(self))
        self.addPage(eidPage(self))

        self.addPage(finalPage(self))
        
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setOption(QtGui.QWizard.IndependentPages,True)
        
        #self.setPixmap(QtGui.QWizard.BannerPixmap,QtGui.QPixmap(':/banner'))
        #self.setPixmap(QtGui.QWizard.BackgroundPixmap, QtGui.QPixmap(':/background'))

        self.setWindowTitle(u"Οδηγός Πρόσληψης Εργαζομένου")

    def accept(self):
        sqlfpr = sqlInsertFpr.format(self.field('epon'),self.field('onom'),self.field('patr'),self.field('mitr'),
                              self.field('sex_id'),self.field('igen'),self.field('afm'),self.field('amka'),
                              self.field('aika'),self.field('pol'),self.field('odo'),self.field('num'),self.field('tk'))  
        fpr_id = dbutils.commitToDb(sqlfpr, self.db)
        sqlpro = sqlInsertPro.format(self.field('prod'),fpr_id,self.field('coy_id'),self.field('eid_id'),
                                     self.field('proy'),self.field('aptyp_id'),self.field('apod'))
        pr_id  = dbutils.commitToDb(sqlpro, self.db)
        print u'Η εγγραφή αποθηκεύτηκε με κωδικούς {0}, {1}'.format(fpr_id,pr_id)
        super(NewEmpWizard, self).accept()
        
class IntroPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setButtonText(QtGui.QWizard.BackButton,u'< Πίσω')
        self.setButtonText(QtGui.QWizard.NextButton,u'Επόμενο >')
        self.setButtonText(QtGui.QWizard.CancelButton,u'Ακύρωση')
        
        self.setTitle(u"Οδηγίες")
        #self.setPixmap(QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(':/watermark1'))

        label = QtGui.QLabel(u"Αυτός ο οδηγός θα δημιουργήσει Νέα Πρόσληψη Εργαζομένου.\n\n "
                u"Για να προχωρήσετε θα πρέπει να εισάγετε τα απαραίτητα δεδομένα \n\n "
                u"Πατήστε δημιουργία στην τελευταία οθόνη για να ολοκληρώσετε.")
        label.setWordWrap(True)
               
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        
        self.setLayout(layout)

class coDataPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(coDataPage, self).__init__(parent)

        self.setButtonText(QtGui.QWizard.BackButton,u'< Πίσω')
        self.setButtonText(QtGui.QWizard.NextButton,u'Επόμενο >')
        self.setButtonText(QtGui.QWizard.CancelButton,u'Ακύρωση')
        
        self.setTitle(u"Εισαγωγή σοιχείων Εργαζομένου")
        self.setSubTitle(u"Συμπληρώστε τα στοιχεία του εργαζομένου")
        #self.setPixmap(QtGui.QWizard.LogoPixmap, QtGui.QPixmap(':/logo1'))
        
        self.labels = OrderedDict()
        self.fields = OrderedDict()
        
        self.labels['epon']= QtGui.QLabel(u"Επώνυμο:")
        self.fields['epon'] = widgets.DbLineEdit()
        

        self.labels['onom']= QtGui.QLabel(u"Όνομα:")
        self.fields['onom'] = widgets.DbLineEdit()
        

        self.labels['patr']= QtGui.QLabel(u"Πατρώνυμο:")
        self.fields['patr'] = widgets.DbLineEdit()
                
        self.labels['mitr']= QtGui.QLabel(u"Μητρώνυμο:")
        self.fields['mitr'] = widgets.DbLineEdit()
        
        self.labels['sex_id']= QtGui.QLabel(u"Φύλο:")
        self.fields['sex_id'] = widgets.DbComboBox([[0,u'Άνδρας'],[1,u'Γυναίκα']])      

        self.labels['igen']= QtGui.QLabel(u"Ημ.Γέννησης:")
        self.fields['igen'] = widgets.DbDateEdit()        

        self.labels['afm']= QtGui.QLabel(u"ΑΦΜ:")
        self.fields['afm'] = widgets.DbLineEdit()
     
        self.labels['doy'] = QtGui.QLabel(u"ΔΟΥ:")
        self.fields['doy'] = widgets.DbLineEdit()
        self.fields['doy'].setReadOnly(True)
        
        doyFindButton = QtGui.QPushButton(u'...')
        doyFindButton.setMaximumSize(QtCore.QSize(20, 50))
        doyLayout = QtGui.QHBoxLayout()
        doyLayout.addWidget(self.fields['doy'])
        doyLayout.addWidget(doyFindButton)
        
        def openFindDlg():
            head = [u'Κωδ',u'ΔΟΥ']
            cw   = [35,300]   
            form = fFindFromList(osyk.doy_list(),head,cw)
            if form.exec_() == QtGui.QDialog.Accepted:
                self.fields['doy'].setText(form.array[1])
                
        doyFindButton.clicked.connect(openFindDlg)
        
                
        self.labels['amka']= QtGui.QLabel(u"ΑΜΚΑ:")
        self.fields['amka'] = widgets.DbLineEdit()

        self.labels['aika']= QtGui.QLabel(u"Αμ.ΙΚΑ:")
        self.fields['aika'] = widgets.DbLineEdit()

        self.labels['pol']= QtGui.QLabel(u"Πόλη:")
        self.fields['pol'] = widgets.DbLineEdit()

        self.labels['tk']= QtGui.QLabel(u"Ταχ.Κωδικός:")
        self.fields['tk'] = widgets.DbLineEdit()
            
        self.labels['odo']= QtGui.QLabel(u"Οδός:")
        self.fields['odo'] = widgets.DbLineEdit()

        self.labels['num']= QtGui.QLabel(u"Αριθμός:")
        self.fields['num'] = widgets.DbLineEdit()  
        
        layout = QtGui.QGridLayout()

        i = j = 0 
        for k in self.labels:
            self.labels[k].setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
            if k == 'doy':
                layout.addWidget(self.labels[k],i,j+0)
                layout.addLayout(doyLayout,i,j+1)
            else:                
                layout.addWidget(self.labels[k],i,j+0)
                layout.addWidget(self.fields[k],i,j+1)
                self.labels[k].setBuddy(self.fields[k])
                self.registerField('%s'% k,self.fields[k],'timi')
            
            if j == 0:
                j=2
            else:
                j=0
                i += 1
        self.setLayout(layout)
        
class eidPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(eidPage, self).__init__(parent)

        self.setButtonText(QtGui.QWizard.BackButton,u'< Πίσω')
        self.setButtonText(QtGui.QWizard.NextButton,u'Επόμενο >')
        self.setButtonText(QtGui.QWizard.CancelButton,u'Ακύρωση')
        
        self.setTitle(u"Ειδικότητα Εργασίας")
        self.setSubTitle(u"Παράρτημα απασχόλησης και ειδικότητα εργασίας")
        #self.setPixmap(QtGui.QWizard.LogoPixmap, QtGui.QPixmap(':/logo1'))

        self.labels = OrderedDict()
        self.fields = OrderedDict() 
      
        self.labels['coy_id']= QtGui.QLabel(u"Περιοχή εργασίας:")
        self.fields['coy_id'] = widgets.DbComboBox([[1,u'Κεντρικό'],])

        self.labels['prod']= QtGui.QLabel(u"Ημ/νία Πρόσληψης:")
        self.fields['prod'] = widgets.DbDateEdit()
                
        self.labels['mereser']= QtGui.QLabel(u"Μέρες εργασίας:")
        self.fields['mereser'] = widgets.WeekDays()
        
        self.labels['dymmy0']= QtGui.QLabel(u"")
        self.fields['dymmy0'] = QtGui.QLabel(u"")
                        
        self.labels['prIn']= QtGui.QLabel(u"Προσέλευση:")
        self.fields['prIn'] = QtGui.QTimeEdit(self) 
        self.fields['prIn'].setDisplayFormat("HH:mm")

        self.labels['prOut']= QtGui.QLabel(u"Αποχώρηση:")
        self.fields['prOut'] = QtGui.QTimeEdit(self) 
        self.fields['prOut'].setDisplayFormat("HH:mm")

        self.labels['diIn']= QtGui.QLabel(u"Διάλειμμα από:")
        self.fields['diIn'] = QtGui.QTimeEdit(self) 
        self.fields['diIn'].setDisplayFormat("HH:mm")

        self.labels['diOut']= QtGui.QLabel(u"Διάλειμμα έως:")
        self.fields['diOut'] = QtGui.QTimeEdit(self) 
        self.fields['diOut'].setDisplayFormat("HH:mm")
        
        self.labels['apType']= QtGui.QLabel(u"Τύπος απασχόλησης:")
        self.fields['apType'] = widgets.DbComboBox([[1,u'Πλήρης απασχόληση'],[2,u'Μερική απασχόληση']])

        self.labels['apdiar']= QtGui.QLabel(u"Διάρκεια απασχόλησης:")
        self.fields['apdiar'] = widgets.DbComboBox([[1,u'Αορίστου χρόνου'],[2,u'Ορισμένου χρόνου']])
                        
        self.labels['eid_id']= QtGui.QLabel(u"Ειδικότητα:")
        self.fields['eid_id'] = widgets.ButtonLineEdit('SELECT id,eidp FROM m12_eid',u'aa|Ειδικότητα',parent.db)

        self.labels['proy']= QtGui.QLabel(u"Προυπηρεσία")
        self.fields['proy'] = widgets.DbSpinBox()
        
        self.labels['aptyp_id']= QtGui.QLabel(u"Τύπος αποδοχών:")
        self.fields['aptyp_id'] = widgets.DbComboBox([[1,u'Μισθός'],[2,u'Ημερομίσθιο'],[3,u'Ωρομίσθιο']])
                    
        self.labels['apod']= QtGui.QLabel(u"Αποδοχές:")
        self.fields['apod'] = widgets.DbDoubleSpinBox()
         
        
        layout = QtGui.QGridLayout()
        i = j = 0 
        for k in self.labels:
            layout.addWidget(self.labels[k],i,j+0)
            layout.addWidget(self.fields[k],i,j+1)
            self.labels[k].setBuddy(self.fields[k])
            self.registerField(k,self.fields[k],'timi')
            if j == 0:
                j=2
            else:
                j=0
                i += 1
        self.setLayout(layout)
           
class finalPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(finalPage, self).__init__(parent)
        
        self.setButtonText(QtGui.QWizard.BackButton,u'< Πίσω')
        self.setButtonText(QtGui.QWizard.FinishButton,u'Ολοκλήρωση')
        self.setButtonText(QtGui.QWizard.CancelButton,u'Ακύρωση')
        
        self.setTitle(u"Ολοκλήρωση πρόσληψης εργαζομένου ")
        #self.setPixmap(QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(':/watermark2'))

        self.label = QtGui.QLabel()
        self.label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initializePage(self):
        finishText = self.wizard().buttonText(QtGui.QWizard.FinishButton)
        finishText.replace('&', '')
        txt = u'<h3>Προσοχή η διαδικασία θα ολοκληρωθεί με τα παρακάτω δεδομένα :</h3>'
        txt += u'Επώνυμο : <b>{0}</b>  '.format(self.field('epon'))
        txt += u'Όνομα : <b>%s</b> <br>' % self.field('onom')
        txt += u'Πατρώνυμο : <b>%s</b>  ' % self.field('patr')
        txt += u'Μητρώνυμο : <b>%s</b><br>' % self.field('mitr')
        txt += u'Φύλο : <b>%s</b>\n' % self.field('sex_id')
        txt += u'Ημερομηνία Γέννησης : <b>%s</b><br>' % self.field('igen')
        txt += u'ΑΦΜ : <b>%s</b><br>' % self.field('afm')
        txt += u'AMKA : <b>%s</b><br>' % self.field('amka')
        txt += u'ΑΜ.ΙΚΑ : <b>%s</b>' % self.field('aika')
        txt += u'Πόλη : <b>%s</b><br>' % self.field('pol')
        txt += u'Οδός : <b>%s</b>' % self.field('odo')
        txt += u'ΑΡθμός : <b>%s</b><br>' % self.field('num')
        txt += u'ΤΚ : <b>%s</b><br>' % self.field('tk')
        txt += u'Μέρες εργασίας : <b>%s</b>' % self.field('mereser')
        
        txt += u'Αποδοχές : <b>%s</b>' % self.field('apod')
        self.label.setText(txt)

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = NewEmpWizard()
    wizard.show()
    sys.exit(app.exec_())
