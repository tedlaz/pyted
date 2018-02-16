"""Text file parser για το ημερολόγιο της singular
"""
import utils as ul


def parsefile(eefile, encoding='WINDOWS-1253'):
    afm_name = {}
    name_afm = {}
    with open(eefile, encoding=encoding) as afile:
        for i, lin in enumerate(afile):
            if len(lin) < 100:
                continue
            afm = lin[67:76]
            try:
                int(afm)
                name = lin[77:91].split('-')[0].strip()
                if afm in afm_name:
                    if name == afm_name[afm]:
                        continue
                    else:
                        print('Error , afm %s with different names' % afm)
                else:
                    afm_name[afm] = name
                    name_afm[name] = afm
            except ValueError:
                continue
    return name_afm


if __name__ == '__main__':
    file = '/home/tedlaz/pelates/2017/d/ee2017d.txt'
    dic = parsefile(file)
    for name, afm in dic.items():
        print(name, afm)
