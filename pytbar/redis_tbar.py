__author__ = 'jawaad'

import codecs
import logging
import redis
from tbar import YuubinBango, unicode_csv_reader
import os.path


class RedisYuubinBango(YuubinBango):
    """Enables the use of Redis-DB with Japanese Postal Code data."""

    def save(self, connection):
        """Uses pipeline / connection sent by default.
        You should use Redis pipelines since they are faster than simple connections"""
        return connection.pipeline().hmset(self.code, self.to_dict())

    @classmethod
    def load(cls, connection, postal_code):
        d = connection.hgetall(postal_code)
        return cls([d[k].decode("utf8") for k in cls.fields()])


def load_data_into_redis(cls, host=6379, port='localhost'):
    """Initializes the Redis DB from initfile in the Redis.config file.
    Download the file from here: http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip"""
    init_file = os.path.join(os.path.dirname(__file__), 'KEN_ALL.CSV')

    try:
        with open(init_file, "r") as f:
            csv_content = codecs.getreader("CP932")(f)
            csv_line_gen = unicode_csv_reader(csv_content)
            pipeline = redis.StrictRedis(port=port, host=host).pipeline()
            for x in csv_line_gen:
                obj = RedisYuubinBango(x)
                obj.save(pipeline)
            f.close()
            pipeline.execute()
    except IOError:
        logging.exception("Could not open Initialization File: {}".format(cls.INIT_FILE))


