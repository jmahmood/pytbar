__author__ = 'jawaad'

import codecs
import logging

from tbar import YuubinBango, unicode_csv_reader


class RedisYuubinBango(YuubinBango):
    """Enables the use of Redis-DB with Japanese Postal Code data."""

    def _save(self, pipeline):
        """Uses pipeline / connection sent by default.
        You should use Redis pipelines since they are faster than simple connections"""
        return pipeline.hmset(self.code, self.to_dict())

    @classmethod
    def save(cls, data, pipeline):
        obj = cls(data)
        obj._save(pipeline)

    @classmethod
    def load(cls, connection, postal_code):
        d = connection.hgetall(postal_code)
        return cls([d[k].decode("utf8") for k in cls.fields()])


def load_data_into_redis(init_file, connection):
    """Initializes the Redis DB from initfile in the Redis.config file.
    Download the file from here: http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip"""
    try:
        with open(init_file, "r") as f:
            csv_content = codecs.getreader("CP932")(f)
            csv_line_gen = unicode_csv_reader(csv_content)
            pipeline = connection.pipeline()
            for x in csv_line_gen:
                RedisYuubinBango.save(x, pipeline)
            pipeline.execute()
    except IOError:
        logging.exception("Could not open Initialization File: {}".format(init_file))


