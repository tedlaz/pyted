# -*- coding: utf-8 -*-
import sqlite3
from u_logger import log
from u_comp import txtEncoded


def backup(dbpath, fileout=None):
    # Convert dbfile to SQL dump file dbfile.sql
    if not dbpath:
        log.error('backup: Database path %s not exists.' % dbpath)
        return False
    try:
        con = sqlite3.connect(dbpath)
        if not fileout:
            fileout = '%s.sql' % dbpath
        with open(fileout, 'w') as f:
            for line in con.iterdump():
                f.write('%s\n' % txtEncoded(line))
    except sqlite3.Error as sqe:
        log.error('backup: error %s' % sqe)
        return False
    con.close()
    log.info('backup: An sql backup of %s saved to %s' % (dbpath, fileout))
    return True
