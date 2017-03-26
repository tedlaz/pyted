# -*- coding: utf-8 -*-


def fun1(vals):
    '''
    About function
    '''
    # pre conditions
    assert vals > 0, 'Input value vals not > 0'

    tmp = vals + 20

    # post conditions
    assert tmp > 20, 'Output value tmp not > 20'

    # return val
    return tmp

if __name__ == '__main__':
    print(fun1(1))
