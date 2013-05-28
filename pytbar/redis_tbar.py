__author__ = 'jawaad'


import codecs
import logging

import redis
from tbar import YuubinBango, unicode_csv_reader

from ConfigParser import ConfigParser


config = ConfigParser()
config.read('redis.config')
PORT = config.get('redis', 'port')
INIT_FILE = config.get('redis', 'initfile')


### REDIS DB CONNECTION SINGLETON
class RedisConnection(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Gets a connection to Redis.
        If you send a port in the first request made to it, it will use that port, otherwise it will use 6379"""

        logging.debug("Retrieving Redis DB connection")

        if not cls._instance:
            logging.debug("Creating new Redis connection")
            cls._instance = redis.Redis(host='localhost', port=int(kwargs.get("port", 6379)))
        return cls._instance


class RedisYuubinBango(YuubinBango):
    """Enables the use of Redis-DB with Japanese Postal Code data."""

    def save(self, pipeline=False):
        """Uses pipeline / connection sent by default.
        You should use Redis pipelines since they are faster than simple connections"""

        if not pipeline:
            pipeline = RedisConnection(port=PORT)

        return pipeline.hmset(self.code, self.to_dict())

    @classmethod
    def load(cls, postal_code):
        connection = RedisConnection(port=PORT)
        d = connection.hgetall(postal_code)
        arr = [d[k].decode("utf8") for k in cls.fields()]
        return cls(arr)


def load_data_into_redis():
    """Initializes the Redis DB from initfile in the Redis.config file.
    Download the file from here: http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip"""
    try:
        with open(INIT_FILE, "r") as f:
            csv_content = codecs.getreader("CP932")(f)
            l = unicode_csv_reader(csv_content)
            pipeline = RedisConnection(port=PORT).pipeline()
            for x in l:
                obj = RedisYuubinBango(x)
                obj.save(pipeline)
            f.close()
            pipeline.execute()
    except IOError:
        logging.exception("Could not open Initialization File: %s" % INIT_FILE)


