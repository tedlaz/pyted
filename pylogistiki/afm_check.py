# -*- coding: utf-8 -*-
from suds.client import Client
#To setup run : sudo pip install suds-jurko


def vatol(afm, countryCode='EL'):
    '''
    VAT Check online
    using SOAP client
    returns dictionary with:
    countryCode, vatNumber, requestDate, valid, name, address
    '''
    url = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    result = {'valid': False}
    try:
        client = Client(url, timeout=10)
        result = client.service.checkVat(countryCode, afm)
    except:
        result['conError'] = True
    return result


if __name__ == '__main__':
    print('Testing function vatchk ...')
    print(vatol('091767623'))
