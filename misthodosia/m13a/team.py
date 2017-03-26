# -*- coding: utf-8 -*-
'''
Created on 21 Απρ 2013

@author: tedlaz
'''
class team():
    def __init_(self):
        self.p01
        self.dr
        self.dc
        self.dl
    
class player():
    def __init__(self,d=None):
        self.name       = d['name']
        self.age        = d['age']
        self.countryid  = d['countryid']
        self.block   #0-20
        self.eksodoi #0-20
        self.reflex  #0-20  
        self.agility #0-20 
        self.tackling #0-20 
        self.heading #0-20 
        self.pasa #0-20 
        self.position  #0-20 
        self.tecknique #0-20 
        self.finish #0-20
        self.speed #0-20 
        self.strength #0-20
         
        self.pos #0 D M F
        self.side #Array 1-4 0 L C R
        self.profStatus # 1-6
        self.experience # 1-10
        self.mentality  # 1-6
        self.form #1-5
        self.satisfaction # 0-100
        self.health # 0-100
        self.physical #0-100
        self.quality #1-10
        self.evolution #0-0.45
        self.talent #String
        
    def gs(self):
        #returns players global value
        pass
    
    def ags(self):
        #returns players affected global value
        pass
    
class diamerisma():
    def __init__(self,aa,orofos,orofosid,owner,user):
        self.id       = aa
        self.orofos   = orofos
        self.orofosid = orofosid
        self.owner    = owner
        self.user     = user
        
    def __str__(self):
        return u'%s %s' % (self.id, self.user)
    
class ejodokat():
    def __init__(self,aa,ejodokatp):
        self.id        = aa 
        self.ejodokatp = ejodokatp
        
    def __str__(self):
        return u'%s %s' % (self.id, self.ejodokatp)
            
class xiliosta():
    def __init__(self, d_id,ej_id,xil):
        self.id            = 0
        self.diamerisma_id = d_id
        self.ejodkat_id    = ej_id
        self.xiliosta      = xil
        
    def __str__(self):
        return u'%s %s = %s' % (self.diamerisma_id, self.ejodkat_id,self.xiliosta)
    
class ejodo():
    def __init__(self):
        self.id
        self.ejodokat_id
        self.date
        self.no
        self.ejodop
        self.ajia
                 
class polykatoikia():
    def __init__(self):
        self.diamerismata = []
        self.ejodakat = []
        self.xiliosta = []
        
    def addDiam(self,diam):
        self.diamerismata.append(diam)
        
    def addEjodaKat(self,ejodakat):
        self.ejodakat.append(ejodakat)
        
    def addXiliosta(self,xiliosta):
        self.xiliosta.append(xiliosta)
            
    def calcKoin(self,listaEjodon):
        for el in listaEjodon:
            
            el.ajia
            
def findPlugins(pluginDir="c:/ted",pluginExtension='.py'):
    import os, sys
    sys.path.insert(0, pluginDir)
    os.chdir(pluginDir)
    pluginFiles = []
    for file in os.listdir("."):
        if file.endswith(pluginExtension):
            ffil = file[:-3]
            impstr = 'import %s as pl1963' % ffil
            exec(impstr)
            pluginFiles.append([pluginDir,ffil,pl1963.name,pl1963.namp])
    return pluginFiles
                       
if __name__ == '__main__':
    d1 = diamerisma(1,1,1,'tedlaz','tedlaz')
    d2 = diamerisma(2,2,1,'popi','popi')
    d3 = diamerisma(3,3,1,'nikos','nikos')
    e1 = ejodokat(1,'Asanser')
    xd1e1 = xiliosta(d1,e1,300)
    xd2e1 = xiliosta(d2,e1,350)
    xd3e1 = xiliosta(d3,e1,350)
    print d1, e1
    pol = polykatoikia()
    pol.addDiam(d1)
    pol.addDiam(d2)
    pol.addDiam(d3)
    pol.addEjodaKat(e1)
    pol.xiliosta = [xd1e1,xd2e1,xd3e1]
    print findPlugins()