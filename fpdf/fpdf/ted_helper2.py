from .fpdf import FPDF
from .ted_helper import Helper


class Tfpdf():
    def __init__(self, ddata={}, filename='test.pdf', orient='P'):
        self.data = ddata
        self.filename = filename
        self.current_page = 0
        self.pdf = FPDF(orientation=orient)
        self.hp = Helper(self.pdf)
        self.pdf.add_font('fn', '', 'times.ttf', True)
        self.pdf.add_font('fi', '', 'timesi.ttf', True)
        self.pdf.add_font('fb', '', 'timesb.ttf', True)
        # self.new_page()  # By default add a new page

    def save(self):
        self.pdf.output(self.filename)

    def new_page(self):
        self.pdf.add_page()
        self.current_page += 1
