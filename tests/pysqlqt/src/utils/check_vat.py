# -*- coding: utf-8 -*-

'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''
# Suds : https://fedorahosted.org/suds
from suds.client import Client, WebFault


def checkVat(afm, countryCode='EL'):
    '''
    using SOAP client
    returns dictionary with:
    countryCode,vatNumber,requestDate,valid,name,address
    '''

    url = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    result = {'valid': False}
    try:
        client = Client(url, timeout=10)
        result = client.service.checkVat(countryCode, afm)

    except WebFault, e:
        print e
        result['conError'] = True
    return result


def is_possible_greek_vat(vat):
    """
    Check Greek vat number against algorithm
    """
    vat = str(vat)
    if len(vat) != 9:
        print("VAT number {0} invalid. Should have 9 digits.".format(vat))
        return False

    if vat.isdigit() is False:
        print("VAT number {0} invalid.Should contain digits only.".format(vat))
        return False
    chcknumbers = [0, 2, 4, 8, 16, 32, 64, 128, 256]
    lchcknumbers = len(chcknumbers)-1
    total = 0
    for i in range(9):
        total += (int(vat[i]) * chcknumbers[lchcknumbers])
        lchcknumbers -= 1
    check_number = int(vat[8])
    rest = total % 11
    if rest == 10:
        rest = 0
    if rest == check_number:
        return True
    else:
        return False


if __name__ == '__main__':
    print(is_possible_greek_vat('046949583'))
    reply = checkVat('094019245')
    print reply
