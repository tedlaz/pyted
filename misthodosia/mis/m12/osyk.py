# -*- coding: utf-8 -*-
'''
Κατεβάζουμε από το site του ΙΚΑ : http://www.ika.gr/gr/infopages/downloads/home.cfm#down2
το τελευταίο ενημερωμένο αρχείο με τον οδηγό σύνδεσης κωδικών.
Αποσυμπιέζουμε στο working dir.
'''
def eid_find(no,fname='./osyk/dn_eid.txt'):
	f = open(fname)
	tstr = 'no value maching'
	for lin in f:
		sp = lin.split('|')
		for i in range(len(sp)):
			sp[i] = sp[i].strip()		
		if no == sp[0]:
			tstr = '%s -> %s'%(sp[0],sp[1].decode('ISO8859-7'))
			break
	f.close()
	return tstr
	
def cad_find(no,fname='./osyk/dn_kad.txt'):
	f = open(fname)
	tstr = 'no value maching'
	for line in f:
		if no == line[:4]:
			tstr = line.decode('ISO8859-7')
			break
	f.close()
	return tstr
	
def kpk_find(no,per='201210',fname='./m12/osyk/dn_kpk.txt'):
	f = open(fname)
	tstr = []
	for lin in f:
		sp = lin.split('|')
		for i in range(len(sp)):
			sp[i] = sp[i].strip()
		if no == sp[0]:
			if per >= sp[5]:
				tstr.append([sp[0],sp[1].decode('ISO8859-7'),sp[2],sp[3],sp[4],sp[5]])
				break
	f.close()
	return tstr
	
def kadeidkpk_find(kad,eid,per='201211',fname='./m12/osyk/dn_kadeidkpk.txt'):
	f = open(fname)
	tstr = ''
	for lin in f:
		sp = lin.split('|')
		for i in range(len(sp)):
			sp[i] = sp[i].strip()	
		if kad == sp[0] and eid == sp[1]:
			if per >= sp[3] and per <= sp[4]:
				tstr += '%s' % sp[2]
				break
	f.close()
	return tstr
	
if __name__ == "__main__":
	print eid_find('913230')
	print cad_find('5540')
	print kadeidkpk_find('5540','913230')
	sa  = kpk_find(kadeidkpk_find('5540','913230'),'201210')
	for e in sa:
		for i in e:
			print i,
		print ''