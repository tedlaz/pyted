# -*- coding: utf-8 -*-
from report_viewer import view_html_report
html_brake = "<p style='page-break-after:always;'>"
html_p = "<p>"


def Single_page_report(value_array, html_template):
        final_text = u''
        pages = len(value_array)

        with open(html_template, 'r') as html_file:
            txt_html = html_file.read().decode('utf-8')

        for i, row_dict in enumerate(value_array):
            final_text += txt_html.format(**row_dict)
            final_line = (html_brake if i+1 < pages else html_p)
            final_text += final_line

        return final_text


if __name__ == '__main__':
    html_template = 'single_page_report.html'
    f1 = {'period': u'Ιανουάριος 2015',
          'typos': u'Μισθοδοσία Περιόδου',
          'co_epon': u'Μαλακόπουλος ΕΠΕ',
          'co_afm': '044444565',
          'co_dra': u'Υπηρεσίες εστίασης',
          'co_addr': u'Αργεντινής 38 14434, Αθήνα',
          'erg_onomatep': u'Θεόδωρος Μαρκόπουλος',
          'erg_pateras': u'Γεράσιμος',
          'erg_afm': '044564112',
          'erg_eid': u'Μάγειρας',
          'misthos': '50,00',
          'meres': '10',
          'apod': '1.000,35',
          'loipa': '0,00',
          'apod_total': '100,35',
          'kratiseis': '20,00',
          'ypoloipo': '85,32',
          'ika': '112,41',
          'foros': '0,00',
          'epid': '0,00',
          'kratiseis': '12,41',
          'imnia': u'Αθήνα 15/3/2015',
          }

    html = Single_page_report([f1, f1], html_template)
    view_html_report(html)
