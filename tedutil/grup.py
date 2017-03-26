# -*- coding: utf-8 -*-


def grup(txtVal):
    '''
    Trasforms a string to uppercase special for Greek comparison
    '''
    ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΊκλμνξοόΌπρσςτυύΎφχψωώΏ"
    ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΦΧΨΩΩΩ"
    ftxt = u''
    for letter in txtVal:
        if letter in ar1:
            ftxt += ar2[ar1.index(letter)]
        else:
            ftxt += letter.upper()
    return ftxt
