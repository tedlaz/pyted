from xml.etree import ElementTree as ET
from operator import itemgetter
import csv
import utils as ul
'''
main xml creation
'''


def keys_in_dict(keylist, adict):
    """Check if keys in keylist exist in adic
    :param keylist: [key1, key2, ...]
    :param adict: {key1: val1, kwy2: val2, ...}
    """
    for key in keylist:
        if key not in adict:
            return False
    return True


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def branch(parent, name, keys, data):
    if not keys_in_dict(keys, data):
        return
    branch = ET.SubElement(parent, name)
    for subelname in keys:
        subel = ET.SubElement(branch, subelname)
        subel.text = str(data[subelname])


def _build_xml(afm, year, month, data, filename):
    packages = ET.Element("packages")
    package = ET.SubElement(packages, "package")
    package.set("actor_afm", afm)
    package.set("month", str(month))
    package.set("year", str(year))
    package.set("branch", "")
    groups = {}
    krev = ['afm', 'amount', 'tax', 'note', 'invoices', 'date']
    kexp = ['afm', 'amount', 'tax', 'note', 'invoices', 'nonObl', 'date']
    kcash = ['cashreg_id', 'amount', 'tax', 'date']
    koexp = ['amount', 'tax', 'date']
    list_afm = []
    for lin in data:

        if lin['typ'] == '1rev':
            if 'rev' not in groups:
                groups['rev'] = ET.SubElement(package, "groupedRevenues")
                groups['rev'].set("action", "replace")
            branch(groups['rev'], 'revenue', krev, lin)

        elif lin['typ'] == '2exp':
            if 'exp' not in groups:
                groups['exp'] = ET.SubElement(package, "groupedExpenses")
                groups['exp'].set("action", "replace")
            lin['nonObl'] = 0
            branch(groups['exp'], 'expense', kexp, lin)

        elif lin['typ'] == '3cash':
            if 'cash' not in groups:
                groups['cash'] = ET.SubElement(package, "groupedCashRegisters")
                groups['cash'].set("action", "replace")
            # cash code here
            lin['cashreg_id'] = lin['afm']
            branch(groups['cash'], 'cashregister', kcash, lin)

        elif lin['typ'] == '4oexp':
            branch(package, 'otherExpenses', koexp, lin)
        if lin['afm'] not in list_afm:
            list_afm.append(lin['afm'])
    indent(packages)
    tree = ET.ElementTree(packages)
    # print(tree.tostring())
    tree.write(filename, xml_declaration=True, encoding='utf-8', method="xml")
    return list_afm


def build_year(afm, data):
    """
    data : {'2017-01-31'}
    """
    trimino = {3: 1, 6: 2, 9: 3, 12: 4}
    fafm = []
    for key, val in data.items():
        year, month, _ = key.split('-')
        month = int(month)
        filename = '%s-%s-%s.xml' % (afm, year, trimino[month])
        lafm = _build_xml(afm, year, month, val, filename)
        fafm += lafm
    afms = list(set(fafm))
    afms.sort()
    for elm in afms:
        print(elm)


def sumdata(data):
    sdic = {}
    for lin in data:
        dat = lin['date']
        typ = lin['typ']
        afm = lin.get('afm', '')
        if afm == '1':  # Για τις πωλήσεις λιανικής χωρίς ταμιακή
            afm = ''
        nte = lin.get('note', '')
        sdic[dat] = sdic.get(dat, {})
        sdic[dat][typ] = sdic[dat].get(typ, {})
        sdic[dat][typ][afm] = sdic[dat][typ].get(afm, {})
        sdic[dat][typ][afm][nte] = sdic[dat][typ][afm].get(
            nte, {'amount': 0, 'tax': 0, 'invoices': 0})
        sdic[dat][typ][afm][nte]['amount'] += ul.dec(lin['amount'])
        sdic[dat][typ][afm][nte]['tax'] += ul.dec(lin['tax'])
        sdic[dat][typ][afm][nte]['invoices'] += 1
    # print(sdic)
    final = {}
    for dat, datv in sdic.items():
        final[dat] = final.get(dat, [])
        for typ, typv in datv.items():
            for afm, afmv in  typv.items():
                for nte, ntev in afmv.items():
                    fdic = {'date': dat}
                    fdic['typ'] = typ
                    fdic['afm'] = afm
                    fdic['note'] = nte
                    fdic['amount'] = ul.dec2grn(ntev['amount'])
                    fdic['tax'] = ul.dec2grn(ntev['tax'])
                    fdic['invoices'] = ntev['invoices']
                    final[dat].append(fdic)
        final[dat] = sorted(final[dat], key=itemgetter('typ', 'afm'))
    return final


def readcsv(filename):
    with open(filename, newline='') as csf:
        spr = csv.DictReader(csf, delimiter='|')
        lst = []
        for row in spr:
            lst.append({'date': row['mdate'], 'typ': row['myft'],
                        'afm': row['afm'], 'note': row['decr'],
                        'amount': row['mposo'], 'tax': row['mfpa']})
        return lst

if __name__ == "__main__":
    # print(keys_in_dict(['a', 'b'], {'c': 1, 'a': 2, 'b': 2}))
    # buildTree()
    cvsf = "/home/tedlaz/pelates/2017/myf2017/myf2017.csv"
    # print(sumdata(fna))
    fna = readcsv(cvsf)
    print(build_year('091767623', sumdata(fna)))
