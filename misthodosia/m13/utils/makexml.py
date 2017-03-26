# -*- coding: utf-8 -*-
header1 = u'''<?xml version="1.0" encoding="utf-8"?>\n'''
header2 = u'''<Ergazomenoi xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www.yeka.gr/SK">\n'''
footer  = u'''</Ergazomenoi>'''
ergHeader                   = u'''  <Ergazomenos xmlns="">\n'''
ergFooter                   = u'''  </Ergazomenos>\n'''

def cTag(tagname, deep=0, val=None):
	spaces = ' ' * deep
	if val:
		tstr = u'%s<%s>%s</%s>\n' % (spaces,tagname,val,tagname)
	else:
		tstr = u'%s<%s />\n' % (spaces,tagname)
	return tstr
	
class erg():
	def __init__(self,afm,amka,amika,epo,ono,pat,mit,sex=u'0',birth=u'15/02/1963'):
		self.aa               = u'1'
		self.afm              = afm
		self.amka             = amka
		self.amika            = amika
		self.eponymo          = epo
		self.onoma            = ono
		self.patronymo        = pat
		self.mitronymo        = mit
		self.sex              = sex
		self.birthdate        = birth
		self.marital_status   = u'1' 
		self.paidiaNo         = u'1'
		self.eidikotita       = u'ΤΟΡΝΑΔΟΡΟΣ'
		self.proslipsiDate    = u'09/11/2012'
		self.proipiresia      = u'0'
		self.anaggeliaDate    = u'09/11/2012'
		self.biblioAnilikouNo = None
		self.adeiaErgasiasNo  = None
		self.oresErgasias     = u'ΠΑΡΑΣΚΕΥΗ - ΣΑΒΒΑΤΟ 22:00 - 3:00'
		self.ores_external    = u'0'
		self.oresDialeima     = None
		self.apodoxes         = u'54,60'
		self.paratiriseis     = None
	def toXml(self):
		ar = []
		ar.append(ergHeader)
		ar.append(cTag('f_aa',4,self.aa))
		ar.append(cTag('f_afm',4,self.afm))
		ar.append(cTag('f_amka',4,self.amka))
		ar.append(cTag('f_amika',4,self.amika))
		ar.append(cTag('f_eponymo',4,self.eponymo))
		ar.append(cTag('f_onoma',4,self.onoma))
		ar.append(cTag('f_onoma_patera',4,self.patronymo))
		ar.append(cTag('f_onoma_miteras',4,self.mitronymo))
		ar.append(cTag('f_sex',4,self.sex))
		ar.append(cTag('f_birthdate',4,self.birthdate))                
		ar.append(cTag('f_marital_status',4,self.marital_status))           
		ar.append(cTag('f_arithmos_teknon',4,self.paidiaNo))
		ar.append(cTag('f_eidikothta',4,self.eidikotita))               
		ar.append(cTag('f_date_proslipsis',4,self.proslipsiDate))		
		ar.append(cTag('f_proipiresia',4,self.proipiresia))              
		ar.append(cTag('f_date_anaggelias',4,self.anaggeliaDate))          
		ar.append(cTag('f_arithmos_vivliou_anilikou',4,self.biblioAnilikouNo))
		ar.append(cTag('f_arithmos_adeias_ergasias',4,self.adeiaErgasiasNo))		
		ar.append(cTag('f_wres_ergasias',4,self.oresErgasias))		
		ar.append(cTag('f_wres_external',4,self.ores_external))            
		ar.append(cTag('f_wres_dialeimatos',4,self.oresDialeima))          
		ar.append(cTag('f_apodoxes',4,self.apodoxes))                
		ar.append(cTag('f_parathrhseis',4,self.paratiriseis))  
		ar.append(ergFooter)
		tstr = u''
		for a in ar:
			tstr += a
		return tstr

def makeXml(ergList):
	tstr = u''
	tstr += header1
	tstr += header2
	i = 1
	for erg in ergList:
		erg.aa = i
		tstr += erg.toXml()
		i += 1
	tstr += footer
	return tstr
if __name__ == '__main__':
	ted =  erg(u'046949583',u'15026350355',u'4560453',u'ΛΑΖΑΡΟΣ',u'ΘΕΟΔΩΡΟΣ',u'ΚΩΝΣΤΑΝΤΙΝΟΣ',u'ΣΤΑΥΡΟΥΛΑ')
	popi = erg(u'094025817',u'20106789556',u'4488822',u'ΔΑΖΕΑ',u'ΚΑΛΛΙΟΠΗ',u'ΝΙΚΟΛΑΟΣ',u'ΜΑΡΙΑ',u'1') 
	print makeXml([ted,popi]).encode('UTF-8')