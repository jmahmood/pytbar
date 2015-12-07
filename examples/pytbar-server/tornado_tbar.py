import logging
import re
import json
from pytbar.redis_tbar import RedisYuubinBango
import redis

import tornado.web
import tornado.options
import tornado.ioloop


class YuubinJsonServer(tornado.web.RequestHandler):

    NON_DECIMAL = re.compile(r'[^\d]+')
    CONN = redis.StrictRedis(port=6379, host='localhost')

    def head(self):
        logging.debug("Postal Code HEAD call")

    def data(self):
        postal_code = self.get_argument("postalcode")
        if not postal_code:
            raise tornado.web.HTTPError(400, "You must include the 'postalcode' "
                                             "variable in the GET command")

        self.NON_DECIMAL.sub('', postal_code)

        if len(postal_code) > 7 or len(postal_code) < 6:
            raise tornado.web.HTTPError(400, "The postal code is invalid. %s" % postal_code)

        return RedisYuubinBango.load(self.CONN, postal_code)

    def get(self):
        logging.debug("Postal Code GET call")
        self.set_header('Content-Type', 'application/javascript')
        self.write(json.dumps(self.data().to_dict()))
