'''
Class to read and write to text files
'''
import decimal


def isNum(val):  # is val number or not ?
    """ use: Returns False if val is not a number , True otherwise
        input parameters :
            1.val : the value to check against.
        output: True or False
        """
    try:
        float(val)
    except ValueError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """ use : Given a number, it returns a decimal with a specific number
        of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or
                int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number
        """
    if poso is None:
        poso = 0
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


class Text_exception(Exception):
    pass

TL, TR, N, D, I = range(5)
dtypos = {0: 'text left',
          1: 'text right',
          2: 'number',  # Always aligned right
          3: 'date',
          4: 'integer'
         }


class Field:
    def __init__(self, name, typos, size=1, fixed_val=None):
        self.name = name
        self.typos = typos
        self.size = size
        self.fixed_val = None
        if self.fixed_val:
            assert self.size == len(str(self.fixed_val))
        if self.typos == D:
            self.size = 10

    def __repr__(self):
        tmpl = 'Field : %s, Type : %s, Size : %s'
        return tmpl % (self.name, dtypos[self.typos], self.size)

    def gtypos(self):
        return dtypos[self.typos]

    def set_val(self, val):
        if self.fixed_val:
            return str(self.fixed_val)
        str_val = str(val)
        len_val = len(str_val)
        # Προσοχή γιατί η len_dif δεν είναι σωστά εδώ ...
        len_dif = self.size - len_val
        if len_dif < 0:
            raise Text_exception('Value size is bigger than field size')
        if self.typos == D:
            if len_val != 10:
                raise Text_exception('Date values are always 10 size')
        if self.typos == TL:
            return str_val + (' ' * len_dif)
        elif self.typos == TR:
            return (' ' * len_dif) + str_val
        elif self.typos == N:
            print(dec(str_val))
            str_val = str(dec(str_val)).replace('.', '')
            dif = self.size - len(str_val)
            return ('0' * dif) + str_val
        elif self.typos == D:
            return str_val
        elif self.typos == I:
            return ('0' * len_dif) + str_val

    def get_val(self, text):
        assert len(text) == self.size
        text = text.strip()
        if self.typos == N:
            integer, decimal = text[:-2], text[-2:]
            return dec('.'.join([integer, decimal]))
        elif self.typos == I:
            return int(text)
        else:
            return text.strip()


class Linetype:
    def __init__(self, name, idv):
        self.name = name
        self.id = idv
        self.lenid = len(str(self.id))
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def size(self):
        tsiz = 0
        for fld in self.fields:
            tsiz += fld.size
        return tsiz + self.lenid

    def set_vals(self, vals):
        assert len(vals) == len(self.fields)
        tstr = '%s' % self.id
        for i, val in enumerate(vals):
            tstr += self.fields[i].set_val(val)
        return tstr

    def get_vals(self, txtline):
        vdic = {}
        i = self.lenid
        for fld in self.fields:
            vdic[fld.name] = fld.get_val(txtline[i: i + fld.size])
            i += fld.size
        return vdic

    def __repr__(self):
        astr = '\n\n'
        astr += '=' * 66 + '\n'
        astr += 'Linetype : %s %s\n' % (self.name, self.id)
        tmpl = '%-30s %-30s %4s \n'
        astr += tmpl % ('name', 'typos', 'size')
        astr += '-' * 66 + '\n'
        for fld in self.fields:
            astr += tmpl % (fld.name, fld.gtypos(), fld.size)
        astr += '-' * 66 + '\n'
        astr += tmpl % ('', '', self.size())
        astr += '\n'
        return astr


class Text_data:
    def __init__(self):
        self.linetypes = {}

    def add_linetype(self, linetype):
        key = linetype.id
        if key in self.linetypes:
            raise Text_exception('Key already exists')
        self.linetypes[key] = linetype

    def __repr__(self):
        tstr = '\n\nText_data linetypes:'
        for key in self.linetypes:
            tstr += self.linetypes[key].__repr__()
        return tstr

    def add_txtline(self, linekey, val_array):
        assert linekey in self.linetypes
        return self.linetypes[linekey].set_vals(val_array)

    def read(self, filename):
        vals = []
        with open(filename) as f:
            while True:
                lin = f.readline()
                # Finish reading file
                if not lin:
                    break
                # Ignore line without data
                if len(lin) < 2:
                    continue
                for key in self.linetypes:
                    if lin.startswith(str(key)):
                        vals.append(self.linetypes[key].get_vals(lin))
        return vals

    def write(self, filename, lines):
        with open(filename, 'w') as f:
            f.write(lines)
