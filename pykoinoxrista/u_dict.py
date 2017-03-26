# -*- coding: utf-8 -*-


def merge_dict_to_listdic(dic, listdic):
    '''
    merge dic values to every dict in listdic
    '''
    for ldic in listdic:
        for key in dic.keys():
            if key in ldic.keys():
                continue  # Do nothing if key already exists
            ldic[key] = dic[key]
    return listdic


if __name__ == '__main__':
    dic = {'a': 10, 'p': 11, 'id': 0}
    ldic = [{'p': 'popi'}, {'b': 'ted'}]
    print(merge_dict_to_listdic(dic, ldic))
    print(ldic)
