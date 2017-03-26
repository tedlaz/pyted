# -*- coding: utf-8 -*-
'''
Created on 17 Ιαν 2014

@author: tedlaz
'''
import dbutils as dbu

sql = u'''
SELECT co.scop,co.jafm, co.sdra, 
coy.sodo || ' ' || coy.snum || ', ' || coy.spol as syad, co.sek, 
er.sono || ' ' || er.sepo as sonep, er.spat, er.sodo || ' ' || er.snum || ', ' || ' ' || er.spol || ', ' || er.jtk as sdkat,er.staf, er.jafm as jafme,
sye.ssye,
strftime('%d/%m/%Y',erp.dpro) as gdpro, erp.eli, erp.tora, erp.imer,erp.napod,erp.nor,
eid.seid,
aptyp.saptyp
FROM co
INNER JOIN coy ON coy.cco=co.id
INNER JOIN erp ON erp.zcoy=coy.id
INNER JOIN er ON erp.zer=er.id
INNER JOIN sye ON erp.csye=sye.id
INNER JOIN eid ON erp.zeid=eid.id
INNER JOIN aptyp ON erp.captyp=aptyp.id
WHERE erp.dpro='{0}'
'''
tmpl =u'''
<p><center><span style=" font-size:14pt; text-decoration: underline;"><b>ΟΡΟΙ ΑΤΟΜΙΚΗΣ ΣΥΜΒΑΣΗΣ ΕΡΓΑΣΙΑΣ ΜΕΡΙΚΗΣ Η ΚΑΙ ΕΚ ΠΕΡΙΤΡΟΠΗΣ ΑΠΑΣΧΟΛΗΣΗΣ</b></span></center><p>
<br>
<p><center><span style=" font-size:12pt;"><b>Ο ΕΡΓΟΔΟΤΗΣ</b></span></center><p>
ΕΠΩΝΥΜΙΑ : {scop}
<br>
ΑΦΜ : {jafm}  ΔΡΑΣΤΗΡΙΟΤΗΤΑ : {sdra}
<br>
ΔΙΕΥΘΥΝΣΗ : {syad}
<br>
ΟΝ/ΜΟ ΕΚΠΡΟΣΩΠΟΥ : {sek}
<br>
<p><center><span style=" font-size:12pt;"><b>Ο ΕΡΓΑΖΟΜΕΝΟΣ</b></span></center><p>
ΟΝ/ΜΟ : {sonep}  ΟΝΟΜΑ ΠΑΤΡΟΣ :  {spat}
<br>
ΔΙΕΥΘΥΝΣΗ ΚΑΤΟΙΚΙΑΣ : {sdkat}
<br>
ΣΤΟΙΧΕΙΑ ΤΑΥΤΟΤΗΤΑΣ : {staf} ΑΦΜ : {jafme}
<br>
<p><center><span style=" font-size:12pt;"><b>ΟΥΣΙΩΔΕΙΣ ΟΡΟΙ</b></span></center><p>
Α. ΕΙΔΟΣ ΣΥΜΒΑΣΗΣ : {ssye}
<ol>
  <li>ΗΜΕΡΟΜΗΝΙΑ ΕΝΑΡΞΗΣ ΣΥΜΒΑΣΗΣ : {gdpro}</li>
  <li>ΗΜΕΡΟΜΗΝΙΑ ΛΗΞΗΣ ΣΥΜΒΑΣΗΣ : {eli}</li>
</ol>
Β. ΧΡΟΝΟΣ ΑΠΑΣΧΟΛΗΣΗΣ : 
<ol>
  <li>ΗΜΕΡΕΣ ΕΒΔΟΜΑΔΙΑΙΩΣ : {imer}</li>
  <li>ΩΡΕΣ ΕΒΔΟΜΑΔΙΑΙΩΣ : {nor}</li>
  <li>ΩΡΑΡΙΟ ΗΜΕΡΗΣΙΑΣ ΑΠΑΣΧΟΛΗΣΗΣ : {tora}</li>
</ol>
Γ. ΤΟΠΟΣ ΠΑΡΟΧΗΣ ΕΡΓΑΣΙΑΣ : {syad}
<br>
Δ. ΕΙΔΙΚΟΤΗΤΑ ΕΡΓΑΖΟΜΕΝΟΥ : {seid}
<br>
Ε. ΑΠΟΔΟΧΕΣ  : {saptyp} {napod} ευρώ
<br>
<br>
ΑΘΗΝΑ {gdpro}
<br>
<center>ΟΙ ΣΥΜΒΑΛΛΟΜΕΝΟΙ</center>
<table width="100%" border="0" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td><center>Ο ΕΡΓΟΔΟΤΗΣ</center></td>
      <td><center>Ο ΕΡΓΑΖΟΜΕΝΟΣ</center></td>
    </tr>
  </tbody>
</table>
<br>
<br>
<br>
<br>
<table width="100%" border="0" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td><center>ΣΦΡΑΓΙΔΑ-ΥΠΟΓΡΑΦΗ</center></td>
      <td><center>ΥΠΟΓΡΑΦΗ    </center></td>
    </tr>
  </tbody>
</table>
'''
'''
<p style='page-break-after:always;'>
'''
reportTitle = u'Σύμβαση'

def toHtml(db='tst.sql3',isoDate='2014-01-25'):
    sqlf = sql.format(isoDate)
    return dbu.fillTemplateFromDb(tmpl,sqlf,db)

def test():
    import sys
    from PyQt4 import QtGui
    import qtreports
    
    app = QtGui.QApplication(sys.argv)
    window = qtreports.rptDlg(toHtml(),reportTitle)
    
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    test()
