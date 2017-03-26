# -*- coding: utf-8 -*-
# Parent of forms
from PyQt4 import QtGui, Qt
from u_logger import log
import u_db_helper as dbh
import u_txt_num as utn


class Fdata(QtGui.QWidget):  # class Fdata(QtGui.QDialog):

    def __init__(self,
                 tables,
                 table,
                 id_=None,
                 ftype='one',
                 visible_buttons=True,
                 invisible_fields=[],
                 parent=None,
                 keyval=[]):
        # ftype : 'one' for one record form,  'many' for many record forms
        QtGui.QWidget.__init__(self, parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.setMinimumWidth(350)

        self.invisible_fields = invisible_fields
        self.parent = parent
        self.keyval = keyval
        self.visible_buttons = visible_buttons
        if parent:
            self.db = parent.db
        else:
            self.db = 'tst.sql3'

        self.ftype = ftype
        self.tables = tables
        self.table = table
        self.meta = self.tables[table]
        self.meta['fields']["id"] = {"lbl": u"AA"}
        self.data = None
        self.id = id_ or 0
        self.title = ''

        # Try to get records from database
        self.get_data()
        self.times = 1
        self.setWindowTitle(self.title)

        self.widgets = []
        self.create_gui()
        self.populate()

    def get_data(self):
        if self.ftype == 'one':
            self.data = dbh.table_val(self.db, self.table, self.id)
            self.title = self.meta['title']
        elif self.ftype == 'manywhere':
            self.data = dbh.table_fkey(self.db, self.table, self.keyval)
            self.title = self.meta['titlep']
        else:
            self.data = dbh.table_vals(self.db, self.table)
            self.title = self.meta['titlep']

    def create_gui(self):
        # create widgets and put them in self.widgets by name
        # self.widgets[fld] = makefld(widg, fld, self)
        raise NotImplementedError

    def populate(self):
        if self.times == 1:
            self.get_data()
        try:
            for i in range(len(self.data['rows'])):
                for field in self.meta['fields']:
                    aval = self.data['rows'][i][field]
                    self.widgets[i][field].set('%s' % aval)
        except IndexError as ier:
            log.critical('Fdata.populate: %s' % ier)

    def saveit(self):
        # To connect with action or button
        # Saves data or searches or ...
        fdic = self.widget_to_dict()  # {fld: value, ..}
        dbh.save_listdic(self.db, self.table, fdic)
        self.closeit()

    def closeit(self):
        if self.parent:
            self.parent.close()
        else:
            self.close()

    def widget_to_dict(self):
        rown = len(self.widgets)
        data_list = []
        for i in range(rown):
            dca = {}
            flag_new = False
            for field in self.meta['order']:
                dca[field] = u'%s' % self.widgets[i][field].get()
                try:
                    oldv = u'%s' % self.data['rows'][i][field]
                except IndexError:
                    flag_new = True
                    continue
                # log.debug('%s %s' % (oldv, dca[field]))
                # Try to save only new or changed records
                if utn.isNum(dca[field]):
                    if '.00' in dca[field]:
                        dca[field] = dca[field][:-3]
                if dca[field] != oldv:
                    flag_new = True
            if flag_new:
                data_list.append(dca)
        # log.debug(data_list)
        # log.debug(self.data)
        return data_list

    def compare_old_new(self):
        # To Do ...
        # dca = self.widget_to_dict()
        for field in self.fields:
            pass
