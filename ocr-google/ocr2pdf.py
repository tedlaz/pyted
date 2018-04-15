import sys
import io
import base64
import json
import requests
import zlib
from string import Template
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from lxml import etree
from lxml import html
from PIL import Image


ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
API_KEY = 'yourApiKeyHere'


def _make_image_data(imgname):
    image_request = ''
    with open(imgname, 'rb') as f:
        ctxt = base64.b64encode(f.read()).decode()
    image_request = {'image': {'content': ctxt},
                     'features': {'type': 'TEXT_DETECTION',
                                  'maxResults': 1},
                     "imageContext": {"languageHints": "el"}
                     }
    return json.dumps({"requests": [image_request]}).encode()


def request_ocr(api_key, imgname):
    response = requests.post(ENDPOINT_URL,
                             data=_make_image_data(imgname),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response


class GCVAnnotation:

    templates = {
        'ocr_page': Template("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="$lang" lang="$lang">
  <head>
    <title>$title</title>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <meta name='ocr-system' content='gcv2hocr.py' />
    <meta name='ocr-langs' content='$lang' />
    <meta name='ocr-number-of-pages' content='1' />
    <meta name='ocr-capabilities' content='ocr_page ocr_carea ocr_line ocrx_word ocrp_lang'/>
  </head>
  <body>
    <div class='ocr_page' lang='$lang' title='bbox 0 0 $page_width $page_height'>
        <div class='ocr_carea' lang='$lang' title='bbox $x0 $y0 $x1 $y1'>$content</div>
    </div>
  </body>
</html>
    """),
        'ocr_line': Template("""
            <span class='ocr_line' id='$htmlid' title='bbox $x0 $y0 $x1 $y1; baseline $baseline'>$content
            </span>"""),
        'ocrx_word': Template("""
                <span class='ocrx_word' id='$htmlid' title='bbox $x0 $y0 $x1 $y1'>$content</span>""")
    }

    def __init__(self,
                 htmlid=None,
                 ocr_class=None,
                 lang='unknown',
                 baseline="0 -5",
                 page_height=None,
                 page_width=None,
                 content=[],
                 box=None,
                 title=''):
        self.title = title
        self.htmlid = htmlid
        self.baseline = baseline
        self.page_height = page_height
        self.page_width = page_width
        self.lang = lang
        self.ocr_class = ocr_class
        self.content = content
        self.x0 = box[0]['x']
        self.y0 = box[0]['y']
        self.x1 = box[2]['x']
        self.y1 = box[2]['y']

    def maximize_bbox(self):
        self.x0 = min([w.x0 for w in self.content])
        self.y0 = min([w.y0 for w in self.content])
        self.x1 = max([w.x1 for w in self.content])
        self.y1 = max([w.y1 for w in self.content])

    def __repr__(self):
        return "<%s [%s %s %s %s]>%s</%s>" % (self.ocr_class, self.x0, self.y0,
                                              self.x1, self.y1, self.content,
                                              self.ocr_class)

    def render(self):
        if type(self.content) == type([]):
            content = "".join(map(lambda x: x.render(), self.content))
        else:
            content = self.content
        return self.__class__.templates[self.ocr_class].substitute(
            self.__dict__, content=content)


def fromResponse(resp, baseline_tolerance=2, **kwargs):
    last_baseline = -100
    page = None
    curline = None
    for anno_idx, anno_json in enumerate(resp['textAnnotations']):
        box = anno_json['boundingPoly']['vertices']
        if anno_idx == 0:
            page = GCVAnnotation(
                ocr_class='ocr_page',
                htmlid='page_0',
                box=box,
                **kwargs
                )
            continue
        word = GCVAnnotation(
            ocr_class='ocrx_word', content=anno_json['description'], box=box)
        if word.y1 - abs(last_baseline) > baseline_tolerance:
            curline = GCVAnnotation(
                ocr_class='ocr_line',
                htmlid="line_%d" % (len(page.content)),
                content=[],
                box=box)
            page.content.append(curline)
            last_baseline = word.y1
        # Δεν είναι σίγουρο ότι χρειάζεται εδώ.
        if not curline:
            continue
        word.htmlid = "word_%d_%d" % (
            len(page.content) - 1, len(curline.content))
        curline.content.append(word)
    for line in page.content:
        line.maximize_bbox()
    page.maximize_bbox()
    if not page.page_width: page.page_width = page.x1
    if not page.page_height: page.page_height = page.y1
    return page.render()


class StdoutWrapper:
    def write(self, data, *args, **kwargs):
        if bytes != str and isinstance(data, bytes):
            data = data.decode('latin1')
        sys.stdout.write(data)


def export2pdf(imagename, html_page, default_dpi):
    """Create a searchable PDF from a pile of HOCR + JPEG"""
    load_invisible_font()
    pdf_file = imagename + '.pdf'
    pdf = Canvas(pdf_file, pageCompression=1)
    pdf.setCreator('hocr-tools')
    pdf.setTitle(imagename)
    dpi = default_dpi
    im = Image.open(imagename)
    w, h = im.size
    try:
        dpi = im.info['dpi'][0]
    except KeyError:
        pass
    width = w * 72 / dpi
    height = h * 72 / dpi
    pdf.setPageSize((width, height))
    pdf.drawImage(imagename, 0, 0, width=width, height=height)
    add_text_layer(pdf, html_page, height, dpi)
    pdf.showPage()
    pdf.save()


def add_text_layer(pdf, html_page, height, dpi):
    """Draw an invisible text layer for OCR data"""
    p1 = re.compile('bbox((\s+\d+){4})')
    p2 = re.compile('baseline((\s+[\d\.\-]+){2})')
    hocr = etree.fromstring(html_page.encode('utf-8'), html.XHTMLParser())
    for line in hocr.xpath('//*[@class="ocr_line"]'):
        linebox = p1.search(line.attrib['title']).group(1).split()
        try:
            baseline = p2.search(line.attrib['title']).group(1).split()
        except AttributeError:
            baseline = [ 0, 0 ]
        linebox = [float(i) for i in linebox]
        baseline = [float(i) for i in baseline]
        for word in line.xpath('.//*[@class="ocrx_word"]'):
            rawtext = word.text_content().strip()
            if rawtext == '':
                continue
            font_width = pdf.stringWidth(rawtext, 'invisible', 8)
            if font_width <= 0:
                continue
            box = p1.search(word.attrib['title']).group(1).split()
            box = [float(i) for i in box]
            b = polyval(baseline, (box[0] + box[2]) / 2 - linebox[0]) + linebox[3]
            text = pdf.beginText()
            text.setTextRenderMode(3)  # double invisible
            text.setFont('invisible', 8)
            text.setTextOrigin(box[0] * 72 / dpi, height - b * 72 / dpi)
            box_width = (box[2] - box[0]) * 72 / dpi
            text.setHorizScale(100.0 * box_width / font_width)
            text.textLine(rawtext)
            pdf.drawText(text)


def polyval(poly, x):
    return x * poly[0] + poly[1]


def load_invisible_font():
    font = """
eJzdlk1sG0UUx/+zs3btNEmrUKpCPxikSqRS4jpfFURUagmkEQQoiRXgAl07Y3vL2mvt2ml8APXG
hQPiUEGEVDhWVHyIC1REPSAhBOWA+BCgSoULUqsKcWhVBKjhzfPU+VCi3Flrdn7vzZv33ryZ3TUE
gC6chsTx8fHck1ONd98D0jnS7jn26GPjyMIleZhk9fT0wcHFl1/9GRDPkTxTqHg1dMkzJH9CbbTk
xbWlJfKEdB+Np0pBswi+nH/Nvay92VtfJp4nvEztUJkUHXsdksUOkveXK/X5FNuLD838ICx4dv4N
I1e8+ZqbxwCNP2jyqXoV/fmhy+WW/2SqFsb1pX68SfEpZ/TCrI3aHzcP//jitodvYmvL+6Xcr5mV
vb1ScCzRnPRPfz+LsRSWNasuwRrZlh1sx0E8AriddyzEDfE6EkglFhJDJO5u9fJbFJ0etEMB78D5
4Djm/7kjT0wqhSNURyS+u/2MGJKRu+0ExNkrt1pJti9p2x6b3TBJgmUXuzgnDmI8UWMbkVxeinCw
Mo311/l/v3rF7+01D+OkZYE0PrbsYAu+sSyxU0jLLtIiYzmBrFiwnCT9FcsdOOK8ZHbFleSn0znP
nDCnxbnAnGT9JeYtrP+FOcV8nTlNnsoc3bBAD85adtCNRcsSffjBsoseca/lBE7Q09LiJOm/ttyB
0+IqcwfncJt5q4krO5k7jV7uY+5m7mPebuLKUea7iHvk48w72OYF5rvZT8C8k/WvMN/Dc19j3s02
bzPvZZv3me9j/ox5P9t/xdzPzPVJcc7yGnPL/1+GO1lPVTXM+VNWOTRRg0YRHgrUK5yj1kvaEA1E
xAWiCtl4qJL2ADKkG6Q3XxYjzEcR0E9hCj5KtBd1xCxp6jV5mKP7LJBr1nTRK2h1TvU2w0akCmGl
5lWbBzJqMJsdyaijQaCm/FK5HqspHetoTtMsn4LO0T2mlqcwmlTVOT/28wGhCVKiNANKLiJRlxqB
F603axQznIzRhDSq6EWZ4UUs+xud0VHsh1U1kMlmNwu9kTuFaRqpURU0VS3PVmZ0iE7gct0MG/8+
2fmUvKlfRLYmisd1w8pk1LSu1XUlryM1MNTH9epTftWv+16gIh1oL9abJZyjrfF5a4qccp3oFAcz
Wxxx4DpvlaKKxuytRDzeth5rW4W8qBFesvEX8RFRmLBHoB+TpCmRVCCb1gFCruzHqhhW6+qUF6tC
pL26nlWN2K+W1LhRjxlVGKmRTFYVo7CiJug09E+GJb+QocMCPMWBK1wvEOfRFF2U0klK8CppqqvG
pylRc2Zn+XDQWZIL8iO5KC9S+1RekOex1uOyZGR/w/Hf1lhzqVfFsxE39B/ws7Rm3N3nDrhPuMfc
w3R/aE28KsfY2J+RPNp+j+KaOoCey4h+Dd48b9O5G0v2K7j0AM6s+5WQ/E0wVoK+pA6/3bup7bJf
CMGjwvxTsr74/f/F95m3TH9x8o0/TU//N+7/D/ScVcA=
""".encode('latin1')
    uncompressed = bytearray(zlib.decompress(base64.decodestring(font)))
    ttf = io.BytesIO(uncompressed)
    setattr(ttf ,"name", "(invisible.ttf)")
    pdfmetrics.registerFont(TTFont('invisible', ttf))


def get_response_from_google(imagename):
    response = request_ocr(API_KEY, imagename)
    if response.status_code != 200 or response.json().get('error'):
        print('Error response')
        return None
    else:
        return response.json()['responses'][0]


def save_file(data, filename):
    with open(filename, 'w') as wfile:
        wfile.write(data)


def main(imgname):
    argdic = {'baseline': '0 0',
              'baseline_tolerance': 2,
              'title': None,
              'lang': 'unknown'}
    if not imgname:
        print("""$ python ocr2pdf.py image.jpg """)
        return
    json_ocr = get_response_from_google(imgname)
    # print(json_ocr)
    html_page = fromResponse(json_ocr, **argdic)
    # print(html_page)
    export2pdf(imgname, html_page, 300)


if __name__ == '__main__':
    main(sys.argv[1])