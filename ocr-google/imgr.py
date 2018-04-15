#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import os
import re
import json
import base64
import requests
import pyexiv2 as ex2
if int(sys.version[0]) == 2:
    from PyQt4.QtGui import QGraphicsView
    from PyQt4.QtGui import QGraphicsScene
    from PyQt4.QtGui import QDialog
    from PyQt4.QtGui import QVBoxLayout
    from PyQt4.QtGui import QHBoxLayout
    from PyQt4.QtGui import QPushButton
    from PyQt4.QtGui import QLabel
    from PyQt4.QtGui import QListWidget
    from PyQt4.QtGui import QListWidgetItem
    from PyQt4.QtGui import QTabWidget
    from PyQt4.QtGui import QWidget
    from PyQt4.QtGui import QTextEdit
    from PyQt4.QtGui import QLineEdit
    from PyQt4.QtGui import QFileDialog
    from PyQt4.QtGui import QInputDialog
    from PyQt4.QtGui import QMessageBox
    from PyQt4.QtGui import QApplication
    from PyQt4.QtGui import QFont
    from PyQt4.QtGui import QRegExpValidator
    from PyQt4.QtGui import QPixmap
    from PyQt4.QtCore import Qt
    from PyQt4.QtCore import QSize
    from PyQt4.QtCore import QMetaObject
    from PyQt4.QtCore import QSettings
    from PyQt4.QtCore import QRegExp
    from PyQt4.QtCore import QVariant
    from PyQt4.QtCore import QDir
elif int(sys.version[0]) == 3:
    from PyQt5.QtWidgets import QGraphicsView
    from PyQt5.QtWidgets import QGraphicsScene
    from PyQt5.QtWidgets import QDialog
    from PyQt5.QtWidgets import QVBoxLayout
    from PyQt5.QtWidgets import QHBoxLayout
    from PyQt5.QtWidgets import QPushButton
    from PyQt5.QtWidgets import QLabel
    from PyQt5.QtWidgets import QListWidget
    from PyQt5.QtWidgets import QListWidgetItem
    from PyQt5.QtWidgets import QTabWidget
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtWidgets import QTextEdit
    from PyQt5.QtWidgets import QLineEdit
    from PyQt5.QtWidgets import QFileDialog
    from PyQt5.QtWidgets import QInputDialog
    from PyQt5.QtWidgets import QMessageBox
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFont
    from PyQt5.QtGui import QRegExpValidator
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtCore import Qt
    from PyQt5.QtCore import QSize
    from PyQt5.QtCore import QMetaObject
    from PyQt5.QtCore import QSettings
    from PyQt5.QtCore import QRegExp
    from PyQt5.QtCore import QVariant
    from PyQt5.QtCore import QDir


ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
SUPPORTED_FORMATS = ('.JPEG', '.JPG')

# Regular expressions
RDATE = r'(?:(?<!\d)\d{1,2}[/-]\d{1,2}[/-]\d{2,4}(?!\d))'
RTIME = r'(?:(?<!\d)\d{1,2}[:]\d{1,2}(?!\d))'
RAFM = r'(?:(?<!\d)\d{9}(?!\d))'


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


def google_ocr(imgname, api_key):
    response = requests.post(ENDPOINT_URL,
                             data=_make_image_data(imgname),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    if response.status_code != 200 or response.json().get('error'):
        print('Error response')
        return ''
    else:
        return response.json()['responses'][0]['fullTextAnnotation']['text']


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


def save_ocr(filename, txtval):
    metadata = ex2.ImageMetadata(filename)
    metadata.read()
    dict_value = {'ocr': txtval}
    jsonv = ''
    if int(sys.version[0]) == 2:
        jsonv = json.dumps(dict_value, ensure_ascii=False, encoding='utf8')
    else:
        jsonv = json.dumps(dict_value, ensure_ascii=False)
    metadata['Exif.Photo.UserComment'] = jsonv
    metadata.write()


def get_image_dict(folder):
    ''' Return {filename: , path:} '''
    image_dict = {}
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file.upper().endswith(SUPPORTED_FORMATS):
                im_path = os.path.join(folder, file)
                image_dict[file] = im_path
    return image_dict


def create_image():
    img = QPixmap(512, 512)
    img.fill()
    return img


def size_to_fit_horizontally(image_size, canvas_size):
    im_w = image_size.width()
    im_h = image_size.height()
    ana = float(im_h) / float(im_w)
    ca_w = canvas_size.width()
    # ca_h = canvas_size.height()
    return QSize(ca_w, int(ca_w * ana))


def parse_invoice(text, synt=[0.13, 0.24], threshold=0.03):
    ftext = ''
    av = text.replace(u'€', '').split()
    # print(av)
    afms = re.findall(r'(?:(?<!\d)\d{9}(?!\d))', str(av))
    dats = re.findall(
        r'(?:(?<!\d)\d{1,2}[/-]\d{1,2}[/-]\d{2,4}(?!\d))', str(av))
    if len(dats) > 0:
        ftext += '\nDATE: %s\n' % dats[0]
    if len(afms) > 1:
        ftext += 'EKDOTIS: %s\n' % afms[0]
        ftext += 'LIPTIS: %s\n' % afms[1]
    found = []
    for el in av:
        try:
            if el[-3] == '.':
                rel = el.replace(',', '')
                a = float(rel)
                if a != 0:
                    found.append(a)
            elif el[-3] == ',':
                rel = el.replace('.', '').replace(',', '.')
                a = float(rel)
                if a != 0:
                    found.append(a)
        except Exception:
            pass
    txt_found = [str(i) for i in found]
    print(txt_found)
    # print('values found', found)
    machfpa = {}
    machsyn = {}
    for i, el in enumerate(found):
        for j, elfpa in enumerate(found):
            if i == j:
                continue
            for syn in synt:
                cfpa = el * syn
                delta = abs(cfpa - elfpa)
                if delta <= threshold:
                    # print('found', el, elfpa)
                    if i in machfpa.keys():
                        deltaold = abs(el * syn - found[machfpa[i]])
                        # print(deltaold, delta)
                        if delta > deltaold:
                            continue
                    machfpa[i] = j
                    txtfpa = '%s' % int(syn * 100)
                    machsyn[txtfpa] = machsyn.get(txtfpa, [])
                    machsyn[txtfpa].append(i)
                    machsyn[txtfpa] = list(set(machsyn[txtfpa]))
    # Filter doublicates
    fdict = {}
    for iposo, ifpa in machfpa.items():
        fposo = found[iposo]
        ffpa = found[ifpa]
        tot = round(fposo + ffpa, 2)
        fdict['%s%s' % (fposo, ffpa)] = [fposo, ffpa, tot]
    # print(fdict)
    # print(machfpa)
    # print(machsyn)
    teliko = {}
    total = 0
    for keyfpa, keynumlist in machsyn.items():
        maxposo = 0
        maxfpa = 0
        for keynum in keynumlist:
            fposo = found[keynum]
            ffpa = found[machfpa[keynum]]
            if fposo > maxposo:
                maxposo = fposo
                maxfpa = ffpa
        tot = round(maxposo + maxfpa, 2)
        teliko[keyfpa] = [maxposo, maxfpa, tot]
        total += tot
    # Print Here ...
    ftext += '\n%3s %12s %12s %12s\n' % ('fpa', 'amount', 'tax', 'total')
    ftext += '-' * 42 + '\n'
    for el in sorted(teliko.keys()):
        val = teliko[el][0]
        fpa = teliko[el][1]
        tot = teliko[el][2]
        ftext += '%3s %12s %12s %12s\n' % (el, val, fpa, tot)
    ftext += '-' * 42 + '\n'
    print(total)
    if str(total) in txt_found:
        ftext += '  Total seems to be ok        %12s\n' % total
    else:
        ftext += '%s' % total
    return ftext


class ImageView(QGraphicsView):
    def __init__(self, picture=None, parent=None):
        """
        QGraphicsView that will show an image scaled to the current widget size
        using events
        """
        super(ImageView, self).__init__(parent)
        self._zoom = 0
        self.set_image(picture)
        QMetaObject.connectSlotsByName(self)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def set_image(self, image):
        if not image:
            self.origPixmap = create_image()
        else:
            self.origPixmap = QPixmap(image)
        self.scene = QGraphicsScene(self)
        self.scene.addPixmap(self.origPixmap)
        self.setScene(self.scene)
        self.centerOn(1.0, 1.0)
        self.setWindowTitle(image or '')
        self.resize_image_to_fit()

    def resize_image_to_fit(self):
        self._zoom = 0
        canvas_size = self.size()
        if len(self.items()) > 0:
            item = self.items()[0]
            image_size = item.pixmap().size()
        else:
            return
        size = size_to_fit_horizontally(image_size, canvas_size)
        # print(image_size, canvas_size, size)
        # size = item.pixmap().size()
        pixmap = self.origPixmap
        pixmap = pixmap.scaled(
            size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.centerOn(1.0, 1.0)
        item.setPixmap(pixmap)

    def resizeEvent(self, event):
        """
        Handle the resize event.
        """
        self._zoom = 0
        size = event.size()
        if len(self.items()) > 0:
            item = self.items()[0]
        else:
            return
        pixmap = self.origPixmap
        pixmap = pixmap.scaled(
            size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.centerOn(1.0, 1.0)
        item.setPixmap(pixmap)

    def wheelEvent(self, event):
        if int(sys.version[0]) == 2:
            delta = event.delta()
        elif int(sys.version[0]) == 3:
            delta = event.angleDelta().y()
        else:
            delta = 0
        size = self.size()
        factor = 0.25
        if delta > 0:
            self._zoom += 1
        else:
            self._zoom -= 1
        # zooming here
        if self._zoom > 0:
            width = size.width() * (1 + factor * self._zoom)
            heigh = size.height() * (1 + factor * self._zoom)
            new_size = QSize(width, heigh)
            item = self.items()[0]
            pixmap = self.origPixmap
            pixmap = pixmap.scaled(
                new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # self.centerOn(1.0, 1.0)
            item.setPixmap(pixmap)
        else:
            self.resize_image_to_fit()


class Form1(QDialog):
    def __init__(self, parent=None):
        super(Form1, self).__init__(parent)
        self.setWindowTitle('Another jpg manager')
        self.settings = QSettings()
        self.folder = ''
        self.image_dict = {}
        main_layout = QVBoxLayout(self)
        h1_layout = QHBoxLayout()
        v0_layout = QVBoxLayout()
        v1_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.img = ImageView()
        self.bopen = QPushButton('select folder')
        self.file_list_label = QLabel('Image Files:')
        self.file_list = QListWidget()
        self.ocr_label = QLabel('embedded text:')
        self.tabw = QTabWidget()
        self.tabw.setMaximumWidth(300)
        self.tab_ocr = QWidget()
        ocr_lay = QVBoxLayout(self.tab_ocr)
        # self.tab_ocr.setLayout(ocr_lay)
        self.tab_inv = QWidget()
        inv_lay = QVBoxLayout(self.tab_inv)
        self.ocr = QTextEdit(self.tab_ocr)
        self.inv = QTextEdit(self.tab_inv)
        self.inv.setLineWrapMode(QTextEdit.NoWrap)
        self.inv.setReadOnly(True)
        mono_font = QFont()
        mono_font.setFamily("DejaVu Sans Mono")
        self.inv.setFont(mono_font)
        ocr_lay.addWidget(self.ocr)
        inv_lay.addWidget(self.inv)

        self.tabw.addTab(self.tab_ocr, 'ocr')
        self.tabw.addTab(self.tab_inv, 'inv')
        self.bocr = QPushButton('do ocr')
        self.bsave_ocr = QPushButton('save text')
        main_layout.addLayout(h1_layout)
        v0_layout.addWidget(self.img)
        v1_layout.addWidget(self.bopen)
        v1_layout.addWidget(self.file_list_label)
        v1_layout.addWidget(self.file_list)
        v1_layout.addWidget(self.ocr_label)
        v1_layout.addWidget(self.tabw)
        v0_layout.addLayout(btn_layout)
        v1_layout.addWidget(self.bocr)
        v1_layout.addWidget(self.bsave_ocr)
        h1_layout.addLayout(v0_layout)
        h1_layout.addLayout(v1_layout)
        self.kod_label = QLabel('Code:')
        self.kod = QLineEdit()
        rval = QRegExp('(\d*)([1-9])(\d*)')
        self.kod.setValidator(QRegExpValidator(rval))
        self.btn_kod = QPushButton('save code')
        btn_layout.addWidget(self.kod_label)
        btn_layout.addWidget(self.kod)
        btn_layout.addWidget(self.btn_kod)
        self.ocr.setMinimumWidth(300)
        self.ocr.setMaximumWidth(300)
        self.file_list.setMaximumWidth(300)
        # connections
        self.file_list.itemSelectionChanged.connect(self.selected)
        self.bopen.clicked.connect(self.get_pictures_to_list)
        self.bsave_ocr.clicked.connect(self.save_ocr_text)
        self.btn_kod.clicked.connect(self.rename_with_kod)
        self.bocr.clicked.connect(self.ocr_online)
        self.ocr.textChanged.connect(self.set_inv)

    def set_inv(self):
        text = u'%s' % self.ocr.toPlainText()
        self.inv.setText(parse_invoice(text))

    def ocr_online(self):
        text = u'%s' % self.ocr.toPlainText()
        if len(text.strip()) == 0:
            if int(sys.version[0]) == 2:
                api_key = '%s' % self.settings.value(
                    "api_key", defaultValue=QVariant('')).toString()
            else:
                api_key = '%s' % self.settings.value(
                    "api_key", defaultValue='')
            if not api_key:
                apitext, ok = QInputDialog.getText(
                    self, "Google API KEY needed",
                    "Your API KEY here:", QLineEdit.Normal,
                    QDir.home().dirName())
                if ok and apitext != '':
                    api_key = '%s' % apitext
                else:
                    return
            filepath = self.current_image_path()
            self.ocr.setText(google_ocr(filepath, api_key))
            self.save_ocr_text()
            self.settings.setValue('api_key', api_key)
            # self.inv.setText(parse_invoice(ocrtext))

    def rename_with_kod(self):
        kodeval = u'%s' % self.kod.text()
        kodeval = kodeval.strip()
        if len(kodeval) == 0:
            return
        file_path = self.current_image_path()
        if len(file_path) == 0:
            return
        old_fname = os.path.basename(file_path)
        dir_name = os.path.dirname(file_path)
        file_parts = old_fname.split('.')
        if len(file_parts) > 2:
            num_part = file_parts[-2]
            try:
                int(num_part)
                return
            except Exception:
                pass
        new_file_parts = [part for part in file_parts[:-1]]
        new_file_parts.append(kodeval)
        new_file_parts.append(file_parts[-1])
        new_file = '.'.join(new_file_parts)
        new_file_path = os.path.join(dir_name, new_file)
        self.image_dict[new_file] = new_file_path
        os.rename(file_path, new_file_path)
        self.file_list.currentItem().setText(new_file)
        self.kod.setText('')

    def save_ocr_text(self):
        text = u'%s' % self.ocr.toPlainText()
        parse_invoice(text)
        # if len(text) > 0:
        save_ocr(self.current_image_path(), text)

    def get_pictures_to_list(self):
        ''' Select a directory, make list of images in it
            and display the first image in the list.
        '''
        folder = str(QFileDialog.getExistingDirectory(
            self, "Select Folder", self.folder))
        if not folder:
            return
        if folder != self.folder:
            self.folder = folder
        else:
            QMessageBox.warning(
                self, 'Already there', 'Folder is currently in use')
            return
        self.image_dict = get_image_dict(self.folder)
        self.file_list.itemSelectionChanged.disconnect()
        self.file_list.clear()
        self.ocr.setText('')
        for img_name in sorted(self.image_dict):
            self.file_list.addItem(QListWidgetItem(img_name))
        self.file_list.itemSelectionChanged.connect(self.selected)
        if len(self.image_dict) > 0:
            self.file_list.setCurrentRow(0)
        else:
            self.set_picture(None)

    def current_image_path(self):
        item = self.file_list.currentItem()
        if not item:
            return ''
        txtval = str(item.text())
        if txtval:
            return self.image_dict[txtval]
        else:
            return ''

    def selected(self):
        self.set_picture(self.current_image_path())

    def set_picture(self, picture=None):
        # picture = '/home/tedlaz/prg/arthro1.jpg'
        self.img.set_image(picture)
        self.setWindowTitle(picture or '')
        ocrtext = read_ocr(picture)
        self.ocr.setText(ocrtext)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("tedlaz")
    app.setOrganizationDomain("tedlaz")
    app.setApplicationName("imgr")
    grview = Form1()
    grview.show()
    sys.exit(app.exec_())
