# -*- coding: utf-8 -*-
'''
Created on 9 Ιαν 2014

@author: tedlaz

Requires suds library : https://fedorahosted.org/suds/

'''

from suds.client import Client

def checkVat(afm,countryCode='EL'):
    '''
    using SOAP client
    returns dictionary with:
    countryCode,vatNumber,requestDate,valid,name,address
    '''    
    url = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    result = {'valid':False}
    try:
        client = Client(url,timeout=10)
        result = client.service.checkVat(countryCode,afm)
    except:
        result['conError'] = True
    return result

if __name__ == '__main__':
    reply = checkVat('997624770')
    print reply
    print 'The Name is ',reply['name']