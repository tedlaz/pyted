#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Page(object):
    def __init__(self, format_name='a4', orientation='portrait'):
        if not isinstance(format_name, basestring):
            self.format_name = 'a4'
        if not isinstance(orientation, basestring):
            self.orientation = 'portrait'

        self.format_name = format_name.lower()
        if self.format_name not in ['a3', 'a4', 'a5', 'letter', 'legal']:
            self.format_name = 'a4'

        self.orientation = orientation.lower()
        if self.orientation not in ['portrait', 'landscape']:
            self.orientation = 'portrait'

    def info(self):
        _str = '\n| Class Page information\n'
        _str += '| ----------------------\n'
        _str += '| Format      : %s\n' % self.format_name
        _str += '| Orientation : %s\n' % self.orientation
        _str += '| Dimensions  : %s X %s\n' % self.get_size()
        return _str

    def get_size(self):
        if self.format_name == 'a3':
            width, height = 841.89, 1190.55
        elif self.format_name == 'a4':
            width, height = 595.28, 841.89
        elif self.format_name == 'a5':
            width, height = 420.94, 595.28
        elif self.format_name == 'letter':
            width, height = 612.00, 792.00
        elif self.format_name == 'legal':
            width, height = 612.00, 1008.00
        else:
            width, height = 595.28, 841.89

        if self.orientation == 'landscape':
            width, height = height, width

        return (width, height)

if __name__ == '__main__':
    print(Page('a3').info())
    print(Page('a3', 'landscape').info())
