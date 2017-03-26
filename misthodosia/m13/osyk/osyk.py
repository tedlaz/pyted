# -*- coding: utf-8 -*-
'''
Κατεβάζουμε από το site του ΙΚΑ : http://www.ika.gr/gr/infopages/downloads/home.cfm#down2
το τελευταίο ενημερωμένο αρχείο με τον οδηγό σύνδεσης κωδικών.
'''
import zipfile
import os
import getFilesFromInternet
osykfile = os.path.join(os.path.dirname(__file__), 'osyk.zip')
#zf = zipfile.ZipFile(osykfile)

if __name__ == "__main__":
	zf = zipfile.ZipFile('osyk.zip')

else:
	if not os.path.exists('osyk/osyk.zip'):
		if not os.path.exists('../osyk/osyk.zip'):
			urlfile = "http://www.ika.gr/gr/infopages/downloads/osyk.zip"
			localfile = 'osyk/osyk.zip'
			getFilesFromInternet.download(urlfile,localfile)
			print 'file Downloaded'
		else:
			zf = zipfile.ZipFile('../osyk/osyk.zip')
	else:
		zf = zipfile.ZipFile('osyk/osyk.zip')
			
WingrEncoding = 'CP1253' # Εναλλακτικά 'ISO8859-7'

#for name in zf.namelist():
#	print name
#	for line in zf.read(name).split("\n"):
#		print line
		
def eid_find(no,fname='dn_eid.txt'):
	tstr = 'no value maching'
	for lin in  zf.read(fname).split("\n"):
		sp = lin.split('|')
		for i in range(len(sp)):
			sp[i] = sp[i].strip()		
		if no == sp[0]:
			tstr = '%s -> %s'%(sp[0],sp[1].decode(WingrEncoding))
			break
	return tstr

	
def cad_find(no,fname='dn_kad.txt'):
	tstr = 'no value maching'
	for line in zf.read(fname).split("\n"):
		if no == line[:4]:
			tstr = line.decode(WingrEncoding)
			break
	return tstr

def cad_list(no=None,fname='dn_kad.txt'):
	tstr = ''
	valArr = []
	for line in zf.read(fname).split("\n"):
			tstr = line.decode(WingrEncoding)
			if no:
				no = str(no)
				if tstr.startswith(no):
					valArr.append(tstr.split('|'))
			else:
				el = tstr.split('|')
				if len(el) > 1:
					valArr.append(tstr.split('|'))
	return valArr

def eid_cad_list(kad=None,per='201201',fname='dn_kadeidkpk.txt'):
	def _eid_find(no,fname='dn_eid.txt'):
		eidArr = []
		for lin in  zf.read(fname).split("\n"):
			lin = lin.decode(WingrEncoding)
			sp = lin.split('|')
			for i in range(len(sp)):
				sp[i] = sp[i].strip()		
			if no == sp[0]:
				el = [sp[0],sp[1]]
				if len(el) == 2:
					eidArr=el
					break
		return eidArr
	arr = []
	for lin in zf.read(fname).split("\n"):
		sp = lin.split('|')
		for i in range(len(sp)):
			sp[i] = sp[i].strip()	
		if kad == sp[0]:
			if per >= sp[3] and per <= sp[4]:
				arr.append(sp[1])
	farr = []
	for eid in arr:
		farr.append(_eid_find(eid))
	return farr
def eid_cad_listFilteredDouble(kad=None,per='201201',fname='dn_kadeidkpk.txt'):	
	arr = eid_cad_list(kad,per,fname)
	lenarr = len(arr)
	finalArr = []
	for i in range(lenarr):
		
		if i > 0:
			if arr[i-1][1] == arr[i][1]:
				finalArr.append([arr[i][0],'%s-%s' % (arr[i][1],i)])
			else:
				finalArr.append(arr[i])
		else:
			finalArr.append(arr[i])
	return finalArr

def kpk_find(no,per='201210',fname='dn_kpk.txt'):
	if not no:
		return ['',]
	tstr = []
	for lin in zf.read(fname).split("\n"):
		sp = lin.split('|')
		for i in range(len(sp)):
			sp[i] = sp[i].strip()
		if no == sp[0]:
			if per >= sp[5]:
				
				tstr.append([sp[0],sp[1].decode(WingrEncoding),sp[2],sp[3],sp[4],sp[5]])
				break
	return tstr
	
def kadeidkpk_find(kad,eid,per,fname='dn_kadeidkpk.txt'):
	''' 
	'''
	tstr = ''
	for lin in zf.read(fname).split("\n"):
		sp = lin.split('|')
		for i in range(len(sp)):
			sp[i] = sp[i].strip()	
		if kad == sp[0] and eid == sp[1]:
			if per >= sp[3] and per <= sp[4]:
				tstr += '%s' % sp[2]
				break
	return tstr

def doy_list(fname='doy.txt'):
	arr = []
	with open(fname) as fil:
		for lin in fil:
			lin = lin.decode('utf-8')
			txt = u'%s' % lin.rstrip('\n')
			arr.append(txt.split('-'))
	return arr

def ika_list(fname='ika.txt'):
	arr = []
	with open(fname) as fil:
		for lin in fil:
			lin = lin.decode('utf-8')
			txt = u'%s' %lin.rstrip('\n')
			arr.append(txt.split('-'))
	return arr

if __name__ == "__main__":
	print eid_find('913240')
	print cad_find('5540')
	print kadeidkpk_find('5530','913230','201211')
	sa  = kpk_find(kadeidkpk_find('5540','913230','201211'),'201211')
	for e in sa:
		for i in e:
			print i,
		print ''
	a = cad_list('55')
	for l in a:
		print l[0],l[1]
	gg = eid_cad_listFilteredDouble('5530')
	for el in gg:
		print el[0],el[1]
	#for el in ika_list():
	#	print el[0],el[1]
