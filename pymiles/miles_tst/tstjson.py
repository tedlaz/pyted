# -*- coding: utf-8 -*-
import json
import io


class JSONConnector:

    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf-8') as f:
            self.data = json.load(f)

    @property
    def parsed_data(self):
        return self.data


def jsonsave(dic, filepath):
    with io.open(filepath, 'w', encoding='utf8') as json_file:
        dt = json.dumps(dic,
                        ensure_ascii=False,
                        encoding='utf8',
                        sort_keys=True,
                        indent=4)
        json_file.write(unicode(dt))
    return True


def jsonread(filepath):
    dic = {}
    with io.open(filepath, 'r',  encoding='utf8') as json_file:
        dic = json.loads(json_file.read())
    return dic

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

if __name__ == '__main__':
    # Next three lines are important for sublime console unicode support
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    ####################################################################
    from tables import tables
    jsonsave(tables, 'aatt.json')
    ff = jsonread('aatt.json')
    print(tables)
    print(json.dumps(tables,
                     ensure_ascii=False,
                     encoding='utf-8',
                     sort_keys=True,
                     indent=3))
