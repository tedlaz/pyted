# -*- coding: utf-8 -*-


def listdim(list1, list2):
    '''
    Συγκρίνει δύο λίστες σε σχέση με τον αριθμό των όρων που έχουν.
    Μετατρέπει αριθμό σε μονοδιάστατη λίστα.
    Αν οι λίστες δεν έχουν την ίδια διάσταση, λαμβάνει σαν αναφορά τη
    μεγαλύτερη διάσταση και προσθέτει μηδενικούς όρους στη μικρότερη λίστα.
    '''
    try:
        len1 = len(list1)
    except:
        len1 = 1
        list1 = [list1, ]
    try:
        len2 = len(list2)
    except:
        len2 = 1
        list2 = [list2, ]
    lenf = len1
    if len1 > len2:
        lenf = len1
        dif = len1 - len2
        for i in range(dif):
            list2.append(0)
    elif len2 > len1:
        lenf = len2
        dif = len2 - len1
        for i in range(dif):
            list1.append(0)
    return list1, list2
