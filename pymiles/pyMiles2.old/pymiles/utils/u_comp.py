# -*- coding: utf-8 -*-
# Compatibility functions between python2 and python3

import sys

pyver = sys.version_info.major


def txtEncoded(atxt):
    if pyver == 3:
        return atxt
    else:
        return atxt.encode('utf-8')
