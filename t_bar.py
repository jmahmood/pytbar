# -*- coding: utf-8 -*-
# Japanese Postal Codes (AKA: Ts with bars on top) Library

import codecs
import csv
import logging
import re
import json

import redis
import tornado.web
from tornado.web import HTTPError
import tornado.ioloop
import tornado.options
from tornado.options import define


### REDIS DB CONNECTION SINGLETON
class RedisConnection(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = redis.Redis(host='localhost', port=6379)
        return cls._instance


### Japanese Post Office provides information as a CSV
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):

    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


### Python's CSV library doesn't work with unicode data.
def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


class YuubinBango(object):
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


class RedisYuubinBango(YuubinBango):
    def save(self, pipeline=False):
        # If there is a pipeline, the pipeline acts as the connection
        if not pipeline:
            pipeline = RedisConnection()
        return self._save(pipeline)

    def _save(self, connection):
        hashname = self.code
        return connection.hmset(hashname, self.to_dict())

    @classmethod
    def load(cls, postalcode):
        connection = RedisConnection()
        d = connection.hgetall(postalcode)
        arr = [d[k].decode("utf8") for k in cls.fields()]
        return cls(arr)


def load_data_into_redis():
    # url = "http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip"
    f = open("/Users/jawaad/Downloads/KEN_ALL.CSV", "r")
    csv_content = codecs.getreader("CP932")(f)
    l = unicode_csv_reader(csv_content)
    pipeline = RedisConnection().pipeline()
    for x in l:
        obj = RedisYuubinBango(x)
        obj.save(pipeline)
    f.close()
    pipeline.execute()


class YuubinJsonServer(tornado.web.RequestHandler):

    def head(self):
        logging.debug("Postal Code HEAD call")

    def data(self):
        postalcode = self.get_argument("postalcode")
        if not postalcode:
            raise HTTPError(400, "You must include the 'postalcode' "
                            "variable in the GET command")

        non_decimal = re.compile(r'[^\d]+')
        non_decimal.sub('', postalcode)

        if len(postalcode) > 7 or len(postalcode) < 6:
            raise HTTPError(400, "The postal code is invalid. %s" % postalcode)

        return RedisYuubinBango.load(postalcode)

    def get(self):
        logging.debug("Postal Code GET call")
        self.set_header('Content-Type', 'application/javascript')
        self.write(json.dumps(self.data().to_dict()))


# Run the Tornado server if this is run directly.
if __name__ == "__main__":
    define("port", default=8887, help="run on the given port", type=int)

    tornado.options.parse_config_file("tbar_server.conf")
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/", YuubinJsonServer),
    ])
    logging.info("starting postal code web server on port %d"
                 % tornado.options.options['port'].value())
    application.listen(int(tornado.options.options['port'].value()))
    tornado.ioloop.IOLoop.instance().start()
