# -*- coding: utf-8 -*-
# This is the place to store table data
#
# lbl : label. Must have a value
# typ : sqltype of field
# qt : txtb(ButtonText), txtl(textLine), txt(Text), txtn(TextNumber)
#      date(Date), ....
# uq: 0 null, 1: not null, 2: table unique, 3: field unique

# Template for new table creation(Copy and uncomment):

#   "tblname": {
#     "title": u"", "titlep": u"",
#     "rpr": "SELECT id, ",
#     "order": [],
#     "fields": {
#       "fld": {"lbl": u"", "typ": "", "qt": "", "uq": 2},
#     }
#   },


app_key = 'tstapp'

app_version = '1.0'

tables = {
  "pro": {
    "title": u"Προμηθευτής", "titlep": u"Προμηθευτές",
    "rpr": "SELECT id, pnam as pro_rp FROM pro",
    "order": ['id', 'pnam', 'vat'],
    "fields": {
      "pnam": {"lbl": u"Προμηθευτής"},
      "vat": {"lbl": u"ΑΦΜ"}
    }
  },
  "eid": {
    "title": u"Είδος", "titlep": u"Είδη",
    "rpr": "SELECT id, eidk || ' ' || eidp as eid_rp FROM eid",
    "order": ["id", "eidp", "eidk"],
    "fields": {
      "eidp": {"lbl": u"Είδος", "uq": 3},
      "eidk": {"lbl": u"Κωδικός", "uq": 3},
    }
  },
  "inv": {
    "title": u"Παραστατικό", "titlep": u"Παραστατικά",
    "rpr": "SELECT id, idate || ' ' || pno as inv_rp FROM inv",
    "order": ["id", "idate", "pno", "pro_id"],
    "fields": {
      "pno": {"lbl": u"Αριθμός", "uq": 2},
      "idate": {"lbl": u"Ημ/νία", "typ": "DATE", "uq": 2, "qt": "date"},
      "pro_id": {"lbl": u"Προμηθευτής", "typ": "INTEGER"}
    }
  },
  "invd": {
     "title": u"Γραμμή παραστατικού", "titlep": u"Γραμμές Παραστατικού",
     "rpr": "SELECT id, eid_id as invd_rp FROM invd",
     "order": ["id", "inv_id", "eid_id", "pos", "timm", "ajia"],
     "fields": {
        "inv_id": {"lbl": u"Παραστατικό", "uq": 2},
        "eid_id": {"lbl": u"Είδος", "uq": 2},
        "pos": {"lbl": u"Ποσότητα", "typ": "NUMERIC", 'qt': 'num'},
        "timm": {"lbl": u"Τιμή Μονάδας", "typ": "NUMERIC", 'qt': 'num'},
        "ajia": {"lbl": u"Αξία", "typ": "NUMERIC", 'qt': 'num'},
     }
  }
}
