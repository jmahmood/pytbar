# -*- coding: utf-8 -*-
# Japanese Postal Codes (AKA: Ts with bars on top) Library

import csv
import logging


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    """This function encodes the CSV data temporarily as UTF-8.
    This is required because Python 2.x's csv library doesn't gracefully deal with Unicode or other formats."""

    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data), dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


### Python's CSV library doesn't work with unicode data.
def utf_8_encoder(unicode_csv_data):
    """Converts every unicode string in an array into a UTF8-encoded string"""

    for line in unicode_csv_data:
        yield line.encode('utf-8')


class YuubinBango(object):
    """This object is a container for the data the Japanese Post Office makes available online."""

    def __init__(self, arr=False, dict=False):
        if arr:
            self.load_array(arr)

    def load_array(self, arr):
        self._arr = arr
        self.nlgc, self.old_code, self.code, \
            self.kk_pref, self.kk_city, self.kk_local, \
            self.pref, self.city, self.local, \
            self.has_multiple_local, \
            self.req_city_entry, \
            self.req_street_entry, \
            self.multiple_locals, \
            self.recently_changed, self._rcr = arr

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    @staticmethod
    def fields():
        """Returns a list of fields and the order in which they appear in the data
        retrieved from the Japanese Post Office"""
        return ['nglc', 'old_code', 'code',
                'kk_pref', 'kk_city', 'kk_local', 'pref', 'city', 'local',
                'has_multiple_local', 'req_city_entry', 'req_street_entry',
                'multiple_locals', 'recently_changed', '_rcr']

    def to_dict(self):
        return dict(zip(self.fields(), self._arr))

    def recently_changed_reason(self):
        return [u"変更なし", u"市政・区政・町政・分区・政令指定都市施行", u"住居表示の実施",
                u"区画整理", u"郵便区調整等", u"訂正", u"廃止(廃止データのみ使用)"
                ][self._rcr]


