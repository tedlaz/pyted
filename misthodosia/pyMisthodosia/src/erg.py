#!/usr/bin/env python
#coding=utf-8

'''
Created on 01 Ιουλ 2011

@author: tedlaz
'''
class Beverage():
    def __init__(self):
        self.desc = 'unknown'
    def getDesc(self):
        return self.desc
    def cost(self):
        return 0

class Espresso(Beverage):
    def __init__(self):
        self.desc = 'Espresso'
    def cost(self):
        return .99
class Mocha():
    def __init__(self,bev):
        self.beverage = bev
    def getDesc(self):
        return self.beverage.getDesc() + ", Mocha"
    def cost(self):
        return .20 + self.beverage.cost()    
class ika():
    def __init__(self):
        self.per = ''
        self.peti = 10
        self.perg = 20
        self.pika = 30
    def getFromDB(self,no=0):
        self.per = 'IKA Mikta'
        self.perg = 10
        self.peti = 20
        self.pika = self.perg + self.peti
    def calc(self,poso):
        ika    = poso * self.pika / 100
        ikaerg = poso * self.perg / 100
        ikaeti = ika - ikaerg
        return ika, ikaerg, ikaeti
class eidikotita():
    def __init__(self,name,isMisthotos=True):
        self.per = name
        self.isMisthotos = isMisthotos
        self.basikosMisthos = 540.24
        self.cod = ''
        self.ika = ika()
    def calcIKA(self):
        return self.ika.calc(self.basikosMisthos)
    def getFromDB(self,no=0):
        pass
class parousia():
    def __init__(self):
        self.per = 'Taktikes apodoxes'
        self.monadaMetrisis = 'meres'
        self.posotis = 25
    def calcApodoxes(self,erg):
        return 0
    def getFromDB(self,no=0):
        pass
class erg():
    def __init__(self):
        self.onoma = 'Ted'
        self.eponymo = 'Lazaros'
        self.eidikotita = eidikotita('logistis')
    def getFromDB(self,no):
        self.onoma = 'Popi'
        self.eponymo = 'Dazea'
if __name__ == '__main__':
    #ted = erg()
    #print ted.eidikotita.per
    #print ted.eidikotita.calcIKA()
    #print ted.eidikotita.ika.calc(1500)
    es = Espresso()
    es = Mocha(es)
    es = Mocha(es)
    print es.getDesc()
    print es.cost()