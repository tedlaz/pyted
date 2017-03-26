# -*- coding: utf-8 -*-
'''
Created on 4 Μαρτίου 2014

@author: tedlaz
'''
import sys
import os
from pyappgen import main
import config as cfg

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    print os.path.dirname(os.path.abspath(__file__))
    main.main(cfg)
    