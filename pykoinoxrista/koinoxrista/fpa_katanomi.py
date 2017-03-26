# -*- coding: utf-8 -*-


def g(dic, key):
    return dic.get(key, 0)


class Entypo():

    def __init__(self, isoz, company_lmoi_fpa, d5400, pyp=0):
        self.isoz = isoz
        self.lmoi_fpa = company_lmoi_fpa
        self.fpad = d5400  # fpa xreosi-pistosi
        self.pyp = pyp
        self.synt = {'301': ['331', 13],
                     '302': ['332', 6.5],
                     '303': ['333', 23],
                     '304': ['334', 8],
                     '305': ['335', 4],
                     '306': ['336', 16],
                     '351': ['371', 13],
                     '352': ['372', 6.5],
                     '353': ['373', 23],
                     '354': ['374', 8],
                     '355': ['375', 4],
                     '356': ['376', 16],
                     '357a': ['377a', 13],
                     '357b': ['377b', 6.5],
                     '357c': ['377c', 23]}

    def calc(self):
        df = {}
        for key in self.isoz.keys():
            if key in self.lmoi_fpa.keys():
                for col in self.lmoi_fpa[key]:
                    df[col] = df.get(col, 0) + self.isoz[key]
            else:
                print('lmos: %s,  is not in the list' % key)

        for key in df.keys():
            if key in self.synt.keys():
                df[self.synt[key][0]] = df[key] * self.synt[key][1] / 100

        # calculate totals
        df['307'] = df.get('301', 0) + df.get('302', 0) + df.get('303', 0) +\
            df.get('304', 0) + df.get('305', 0) + df.get('306', 0)
        df['337'] = df.get('331', 0) + df.get('332', 0) + df.get('333', 0) +\
            df.get('334', 0) + df.get('335', 0) + df.get('336', 0)

        df['311'] = df['307'] + df.get('308', 0) + df.get('309', 0) +\
            df.get('310', 0)

        df['357'] = g(df, '357a') + g(df, '357b') + g(df, '357c')
        df['377'] = g(df, '377a') + g(df, '377b') + g(df, '377c')
        fd = {}
        # create a dictionary with text keys
        for key in df.keys():
            nkey = 'i%s' % key
            fd[nkey] = df[key]
        return fd


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    l = {'20.01.00.023': ['353'],
         '24.01.00.023': ['353'],
         '24.02.00.000': ['353', '303', '341'],
         '25.01.00.023': ['353'],
         '25.02.00.000': ['353', '303', '341'],
         '70.02.00.000': ['309', '342'],
         '71.00.00.023': ['303'],
         '71.00.01.000': ['309'],
         '71.00.01.016': ['306'],
         '71.00.01.023': ['303'],
         '73.00.01.023': ['303'],
         '6.13': ['357a'],
         '6.23': ['357c']
         }

    vl = {'20.01.00.023': 1589.97,
          '24.01.00.023': 64884.39,
          '24.02.00.000': 1323.6,
          '25.01.00.023': 6613.98,
          '25.02.00.000': 8,
          '70.02.00.000': 125.02,
          '71.00.00.023': 12118.95,
          '71.00.01.000': 26455,
          '71.00.01.016': 7828.68,
          '71.00.01.023': 59629.29,
          '73.00.01.023': -652.69,
          '6.13': 1000.08,
          '6.23': 8683.96
          }

    ent = Entypo(vl, l, 100, 0)

    ddd = ent.calc()

    print(ddd)
    print("edo {i357a}, kai {i377a}".format(**ddd))
