"""Module to calculate Asfalistika Tameia"""
import utils as ul


def ika(erg):
    """
    Social sequrity calculation
    """
    cio = ul.DicDec()
    ilb = {}
    cio['poso'] = erg['poso']
    ilb['poso'] = 'Ποσό για ΙΚΑ'
    # Άν τα ποσοστά είναι μεγαλύτερα του 1 θεωρούμε ότι είναι εκφρασμέντα
    # επι τοις εκατό και τα μετατρέπουμε σε δεκαδικά < 1
    cio['pika'] = erg['pika'] if erg['pika'] < 1 else erg['pika'] / 100.0
    ilb['pika'] = 'Ποσοστό ΙΚΑ'
    cio['pikae'] = erg['pikae'] if erg['pikae'] < 1 else erg['pikae'] / 100.0
    ilb['pikae'] = 'Ποσοστό ΙΚΑ εργαζομένου'
    # Calculate here ...
    cio['pikar'] = cio['pika'] - cio['pikae']
    ilb['pikar'] = 'Ποσοστό ΙΚΑ εργoδότη'
    cio['ika'] = cio['poso'] * cio['pika']
    ilb['ika'] = 'ΙΚΑ'
    cio['ikae'] = cio['poso'] * cio['pikae']
    ilb['ikae'] = 'ΙΚΑ εργαζόμενου'
    cio['ikar'] = cio['ika'] - cio['ikae']
    ilb['ikar'] = 'ΙΚΑ εργοδότη'
    return cio, ilb
