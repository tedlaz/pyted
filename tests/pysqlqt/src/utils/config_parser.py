#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser


def add_and_save(parameter, value, section='Main', ini_file='config.ini'):
    conf = ConfigParser.ConfigParser()
    conf.read(ini_file)
    try:
        conf.add_section(section)
    except ConfigParser.DuplicateSectionError:
        pass
    conf.set(section, parameter, value)
    with open(ini_file, 'w') as fileconfig:
        conf.write(fileconfig)


def read_parameter(parameter, section, ini_file='config.ini'):
    conf = ConfigParser.ConfigParser()
    if conf.read(ini_file):
        try:
            return conf.get(section, parameter)
        except ConfigParser.NoOptionError:
            return ''
        except ConfigParser.NoSectionError:
            return ''
    else:
        return ''


if __name__ == '__main__':
    ini_fil = 'test.ini'
    add_and_save('name', 'ted', 'Personal', ini_fil)
    print(read_parameter('name', 'Personal', ini_fil))
    print(read_parameter('epon', 'Personal', ini_fil))
    print(read_parameter('name', 'Private', ini_fil))
    add_and_save('epon', 'lazaros', 'Private', ini_fil)
