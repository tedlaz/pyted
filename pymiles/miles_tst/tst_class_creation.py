# -*- coding: utf-8 -*-


class Erg(object):

    """
    test class for all ...
    """

    def __init__(self, ddic):
        # required parameters
        self.epo = ddic['epo']
        self.ono = ddic['ono']

        # optional parameters
        self.pat = ddic.get('pat', '')

    def __repr__(self):
        return '%s %s %s' % (self.epo, self.ono, self.pat)


if __name__ == '__main__':
    ted = Erg({'epo': 'Lazaros', 'ono': 'Ted', 'pat': 'Kostas'})
    print(ted)
