# -*- coding: utf-8 -*-
import os
import re
import decimal
import json
import pyexiv2 as ex2
import itertools


SUPPORTED_FORMATS = ('.JPEG', '.JPG')

# Regular expressions
RDATE = r'(?:(?<!\d)\d{1,2}[/-]\d{1,2}[/-]\d{2,4}(?!\d))'
RTIME = r'(?:(?<!\d)\d{1,2}[:]\d{1,2}(?!\d))'
RAFM = r'(?:(?<!\d)\d{9}(?!\d))'
RNUM = r'(?:(?<!\d)\d{1,3}(?:[.,]{0,}\d{3})*[.,]\d{2}(?!\d))'
RINUM = r'(?:(?<![\d.,])\d{3,8}(?![\d.,]))'


def dec(poso=0, decimals=2):
    """Returns a decimal. If poso is not a number or None returns dec(0)"""
    tmp = decimal.Decimal(poso)
    qval = decimal.Decimal(10) ** (-1 * decimals)
    return tmp.quantize(qval, rounding=decimal.ROUND_HALF_UP)


def iso_date(date):
    try:
        day, month, year = date.replace('/', '-').split('-')
        year = '20%s' % year if len(year) == 2 else year
        month = '0%s' % month if len(month) == 1 else month
        day = '0%s' % day if len(day) == 1 else day
        return '-'.join([year, month, day])
    except Exception:
        return ''


def get_image_dict(folder):
    ''' Return {filename: , path:} '''
    image_dict = {}
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file.upper().endswith(SUPPORTED_FORMATS):
                im_path = os.path.join(folder, file)
                image_dict[file] = im_path
    return image_dict


def read_ocr(filename):
    if not filename:
        return ''
    metadata = ex2.ImageMetadata(filename)
    metadata.read()
    try:
        jdata = metadata['Exif.Photo.UserComment'].value
    except ValueError:
        return ''
    except KeyError:
        return ''
    try:
        return json.loads(jdata)['ocr']
    except ValueError:
        return jdata


def clean_numbers(text_numbers):
    found = []
    for el in text_numbers:
        try:
            if el[-3] == '.':  # 123,456.78 becomes 123456.78
                rel = el.replace(',', '')
                a = dec(rel)
                if a != 0:  # exclude zero values
                    found.append(a)
            elif el[-3] == ',':  # 123.456,78 becomes 123456.78
                rel = el.replace('.', '').replace(',', '.')
                a = dec(rel)
                if a != 0:
                    found.append(a)
        except Exception:
            pass
    found = list(set(found))
    return sorted(found, reverse=True)


class InvoiceLine():
    fmt = '%4s %12s %12s %12s'
    tit = fmt % ('FPA%', 'Amount', 'Tax', 'Total')

    def __init__(self, fpa, amount, tax):
        self.fpa = fpa
        self.amount = dec(amount)
        self.tax = dec(tax)

    @property
    def total(self):
        return self.amount + self.tax

    def __repr__(self):
        return self.fmt % (self.fpa, self.amount, self.tax, self.total)


class Invoice():
    def __init__(self, date, time, number, afm_ekdoti, afm_lipti,
                 note='normal', lines=None):
        self.date = date
        self.time = time
        self.number = number
        self.note = note
        self.afm_ekdoti = afm_ekdoti
        self.afm_lipti = afm_lipti
        self.lines = lines or []

    def add_line(self, line):
        assert isinstance(line, InvoiceLine)
        self.lines.append(line)

    @property
    def total_amount(self):
        return sum([i.amount for i in self.lines])

    @property
    def total_tax(self):
        return sum([i.tax for i in self.lines])

    @property
    def total_total(self):
        return sum([i.total for i in self.lines])

    @property
    def to_dict(self):
        tdic = {'date': self.date, 'time': self.time, 'number': self.number,
                'note': self.note, 'afm_ekdoti': self.afm_ekdoti,
                'afm_lipti': self.afm_lipti, 'amount': self.total_amount,
                'tax': self.total_tax, 'lines': []}
        for line in self.lines:
            tdic['lines'].append({'fpa': line.fpa, 'amount': line.amount,
                                  'tax': line.tax})
        return tdic

    def __repr__(self):
        txt = 'DATE    : %s\n' % self.date
        txt += 'TIME    : %s\n' % self.time
        txt += 'EKDOTIS : %s\n' % self.afm_ekdoti
        txt += 'LIPTIS  : %s\n' % self.afm_lipti
        txt += InvoiceLine.tit + '\n'
        txt += '\n'.join([i.__repr__() for i in self.lines])
        txt += '\n' + InvoiceLine.fmt % (
            'tot', self.total_amount, self.total_tax, self.total_total)
        return txt


def parse_invoice(text, synt=[13, 24], threshold=0.03):
    # print(text)
    dsynt = {str(n): dec(n / 100.0) for n in synt}
    threshold = dec(threshold)
    txt = text.replace(u'€', ' ')
    # print(av)
    obj = {}
    afms = re.findall(RAFM, txt)
    dats = re.findall(RDATE, txt)
    tims = re.findall(RTIME, txt)
    nums = re.findall(RNUM, txt)
    # invn = re.findall(RINUM, txt)
    date = iso_date(dats[0] if len(dats) > 0 else '')
    time = tims[0] if len(tims) > 0 else ''
    afme = afms[0] if len(afms) > 1 else ''
    afml = afms[1] if len(afms) > 1 else ''
    print('\nDATE    : %s' % date)
    print('TIME    : %s' % time)
    print('EKDOTIS : %s' % afme)
    print('LIPTIS  : %s' % afml)
    obj['date'] = date
    obj['time'] = time
    obj['afm_ekdoti'] = afme
    obj['afm_lipti'] = afml
    obj['lines'] = []
    found = clean_numbers(nums)
    # print(' '.join([str(i) for i in found]))
    mval = {}
    # iters = 0
    for i, el in enumerate(found):
        for syn in dsynt:
            cfpa = dec(el * dsynt[syn])
            for elfpa in found[i + 1:]:
                delta = abs(cfpa - elfpa)
                # iters += 1
                if delta <= threshold:
                    mval[syn] = mval.get(syn, [])
                    mval[syn].append([el, elfpa, el + elfpa, delta])
    # for key in mval:
    tval = tfpa = ttot = dec(0)
    strt = '%3s %12s %12s %12s %12s'
    for key in mval:
        val = mval[key][0]
        tval += val[0]
        tfpa += val[1]
        ttot += val[2]
        print(strt % (key, val[0], val[1], val[2], val[3]))
    print(strt % ('tot', tval, tfpa, ttot, ''))
    print('ok' if ttot in found else 'not ok')
    # print(iters)


def parse_numbers(num_dic, fpa_synt, threshold=0.02):
    pfpas = {str(n): dec(n / 100.0) for n in fpa_synt}
    numbs = [dec(n) for n in num_dic]
    numbs.sort(reverse=True)
    items = []
    # delta = {}
    for i, num1 in enumerate(numbs):
        for fpa, pfpa in pfpas.items():
            vfpa = dec(num1 * pfpa)
            for j, num2 in enumerate(numbs):
                if abs(vfpa - num2) <= threshold:
                    items.append((fpa, i, j))
    uitems = unique(items)
    flist = []
    total_values = []
    for item in uitems:
        ttot = ['  ', dec(0), dec(0), dec(0)]
        tdic = {}
        for tupl in item:
            tfpa, sval, sfpa = tupl[0], numbs[tupl[1]], numbs[tupl[2]]
            stot = sval + sfpa
            ttot[1] += sval
            ttot[2] += sfpa
            ttot[3] += stot
            tdic[tfpa] = {'amount': sval, 'tax': sfpa, 'tot': stot}
        tdic['tamount'] = ttot[1]
        tdic['ttax'] = ttot[2]
        tdic['ttot'] = ttot[3]
        if ttot[3] in numbs:
            if tdic not in flist:
                flist.append(tdic)
                total_values.append(ttot[3])
    if flist:
        return_dicts = []
        maxtot = max(total_values)
        for adic in flist:
            if adic['ttot'] == maxtot:
                return_dicts.append(adic)
        return return_dicts
    return None


def unique(vals):
    # vals = ((a1,b1,c1,...), (a2,b2,c2,..), ...(an, bn,cn,..))
    comps = [i for j in range(2, 0, -1)
             for i in itertools.combinations(vals, j)]
    final = []
    for comp in comps:
        flist = [j for i in comp for j in i]
        if len(flist) == len(set(flist)):
            final.append(comp)
    return final


def prndic(rdic):
    tml = '%-5s %12s %12s %12s'
    for key, val in rdic.items():
        if isinstance(val, dict):
            print(tml % (key, val['amount'], val['tax'], val['tot']))
    print(tml % ('Total', rdic['tamount'], rdic['ttax'], rdic['ttot']))


def parse_images(path):
    images = get_image_dict(path)
    for img_path in sorted(images.values()):
        ocr = read_ocr(img_path)
        nums = re.findall(RNUM, ocr)
        cnums = clean_numbers(nums)
        print(img_path)
        # print([str(i) for i in cnums])
        if cnums:
            fdi = parse_numbers(cnums, [13, 24])
            if fdi:
                print('Number of maches: %s' % len(fdi))
                prndic(fdi[0])
            else:
                print('No Fpa')
                print([str(i) for i in cnums])
        else:
            print('No ocr data')
        print('=' * 80)


if __name__ == '__main__':
    path = '/home/tedlaz/Downloads/180326/'
    parse_images(path)
