'''
Helper class for easy fpdf form creation
'''


class Helper():
    def __init__(self, pdfo):
        self.pdo = pdfo
        self.left_margin = 10.0
        self.top_margin = 10.0
        self.p_width = 190
        self.p_height = 260.0

    def line(self, x1, y1, x2, y2, w=0.0):
        self.pdo.set_line_width(w)
        self.pdo.line(x1, y1, x2, y2)

    def _txt(self, x, y, txt, align, font, fontsize):
        self.pdo.set_font(font, '', fontsize)
        self.pdo.set_xy(x, y)
        self.pdo.cell(ln=0, h=1.0, align=align, w=0.1, txt=txt, border=0)

    def txtc(self, x, y, txt, fontsize=10.0):
        self._txt(x, y, txt, 'C', 'fn', fontsize)

    def txtcb(self, x, y, txt, fontsize=10.0):
        self._txt(x, y, txt, 'C', 'fb', fontsize)

    def txtci(self, x, y, txt, fontsize=10.0):
        self._txt(x, y, txt, 'C', 'fi', fontsize)

    def txtl(self, x, y, txt, fontsize=10.0):
        self._txt(x, y, txt, 'L', 'fn', fontsize)

    def txtlb(self, x, y, txt, fontsize=10.0):
        self._txt(x, y, txt, 'L', 'fb', fontsize)

    def txtli(self, x, y, txt, fontsize=10.0):
        self._txt(x, y, txt, 'L', 'fi', fontsize)

    def txtr(self, x, y, txt, fontsize=10.0):
        self._txt(x, y, txt, 'R', 'fn', fontsize)

    def txtrb(self, x, y, tx, fontsize=10.0):
        self._txt(x, y, txt, 'R', 'fb', fontsize)

    def txtri(self, x, y, txt, fontsize=10.0):
        self._txt(x, y, txt, 'R', 'fi', fontsize)

    def num(self, x, y, tx, fsi=10.0, wi=0.1, bor=0):
        self.pdo.set_font('arial', '', fsi)
        self.pdo.set_xy(x, y)
        self.pdo.cell(ln=0, h=1.0, align='R', w=wi, txt=tx, border=bor)

    def numb(self, x, y, tx, fsi=10.0, wi=0.1, bor=0):
        self.pdo.set_font('arial', 'B', fsi)
        self.pdo.set_xy(x, y)
        self.pdo.cell(ln=0, h=1.0, align='R', w=wi, txt=tx, border=bor)

    def numi(self, x, y, tx, fsi=10.0, wi=0.1, bor=0):
        self.pdo.set_font('arial', 'I', fsi)
        self.pdo.set_xy(x, y)
        self.pdo.cell(ln=0, h=1.0, align='R', w=wi, txt=tx, border=bor)

    def rect(self, x1, y1, w, h, wi=0.0):
        self.pdo.set_line_width(wi)
        self.pdo.rect(x1, y1, w, h, style='')

    def hline(self, y, x1, x2, width=0.0):
        self.pdo.set_line_width(width)
        self.pdo.line(x1, y, x2, y)

    def vline(self, x, y1, y2, width=0.0):
        self.pdo.set_line_width(width)
        self.pdo.line(x, y1, x, y2)

    def donti(self, x=15, y=180, mikos=35, theseis=5, platos=4):
        bima = mikos / theseis
        self.line(x, y, x+mikos, y)
        for i in range(theseis+1):
            self.line(x+(i*bima), y-platos, x+(i*bima), y)

    def boxes(self, x=15, y=180, mikos=35, theseis=5, platos=4):
        bima = mikos / theseis
        self.line(x, y - platos, x + mikos, y - platos)
        self.line(x, y, x + mikos, y)
        for i in range(theseis+1):
            self.line(x+(i*bima), y-platos, x+(i*bima), y)

    def boxetit(self, x, y, title, value, siz=6):
        val = '%s' % value
        theseis = len(val)
        titls = len(title) * 3
        tmikos = theseis * siz + titls
        self.line(x, y - siz, x + tmikos, y - siz)
        self.line(x, y, x + tmikos, y)
        self.line(x, y - siz, x, y)
        for i in range(theseis + 1):
            self.line(x+titls+(i*siz), y-siz, x+titls+(i*siz), y)
        self.txtcb(x + (titls / 2), y - (siz / 2), title, 12)
        for i, el in enumerate(value):
            self.txtcb(x + titls + i * siz + (siz / 2), y - (siz / 2), el, 12)

