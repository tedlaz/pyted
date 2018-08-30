import requests
from bs4 import BeautifulSoup as bs
import csv


PAGE = ("http://www.xe.gr/property/search?Geo.area_id_new__hierarchy="
        "82196&Item.type=31945&System.item_type=re_residence&"
        "Transaction.type_channel=117518&per_page=50&page=%s")
PAGEBASE = "http://www.xe.gr"
FIELDS = ('typos', 'perioxi', 'tm', 'ajia', 'ajiatm', 'html')


def scrap2csv(filename, pages=1, thres=200, apo=0):
    """thres: Το όριο απόρριψης εγγραφής (τιμή/τμ)
    """
    stt = 'Page %s/%s(found %s/%s)'
    fil = csv.writer(open(filename, 'x'))
    fil.writerow(FIELDS)
    total_prop_found = 0
    for num in range(apo, pages):
        typ = ''
        per = ''
        tme = ajia = ajt = 0
        htt = ''
        fnum = num + 1
        page_properties_found = 0
        page = requests.get(PAGE % fnum)
        soup = bs(page.text, 'html.parser')
        for el in soup.find_all(class_='lazy r'):
            try:
                ajiat = el.find(class_='r_price')
                if not ajiat:
                    continue
                ajiat = ajiat.contents[0]
                ajia = int(ajiat.replace('€', '').strip().replace('.', ''))
                tmet = el.find(class_='r_stats').find_all('li')
                if len(tmet) < 2:
                    continue
                tme = int(tmet[1].contents[0].split('\xa0')[0])
                ajt = ajia // tme
                if ajt < thres:
                    continue

                class_rt = el.find(class_='r_t')
                if not class_rt:
                    class_rt = el.find(class_='r_t prem')
                if not class_rt:
                    continue
                hrf = class_rt.get('href')
                _, typ, per, *_ = hrf.split('|')
                htt = PAGEBASE + hrf
                fil.writerow([typ, per, tme, ajia, ajt, htt])
                page_properties_found += 1
            except Exception as err:
                print(err)
                continue
        total_prop_found += page_properties_found
        print(stt % (fnum, pages, page_properties_found, total_prop_found))
    print("Finished, found %s total properties" % total_prop_found)


if __name__ == '__main__':
    filename = 'xrisi-eykairia-diamerismata-athina3.csv'
    scrap2csv(filename, pages=3000, apo=2000)
