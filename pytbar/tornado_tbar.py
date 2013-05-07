import logging
import re
import json

import tornado.web
import tornado.options
import tornado.ioloop

from redis_tbar import *


class YuubinJsonServer(tornado.web.RequestHandler):

    def head(self):
        logging.debug("Postal Code HEAD call")

    def data(self):
        postalcode = self.get_argument("postalcode")
        if not postalcode:
            raise tornado.web.HTTPError(400, "You must include the 'postalcode' "
                                             "variable in the GET command")

        non_decimal = re.compile(r'[^\d]+')
        non_decimal.sub('', postalcode)

        if len(postalcode) > 7 or len(postalcode) < 6:
            raise tornado.web.HTTPError(400, "The postal code is invalid. %s" % postalcode)

        return RedisYuubinBango.load(postalcode)

    def get(self):
        logging.debug("Postal Code GET call")
        self.set_header('Content-Type', 'application/javascript')
        self.write(json.dumps(self.data().to_dict()))
