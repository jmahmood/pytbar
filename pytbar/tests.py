import unittest
import os.path
import redis
import redis_tbar

__author__ = 'jawaad'


class TestSuccessfulUploads(unittest.TestCase):
    """
    Currently the repository for all tests related to pytbar.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        """
        Setup API key / Flickr Token for additional logins.
        :return:
        """
        self.connection = redis.StrictRedis(port=6379, host='localhost')

        init = {
            'init_file': os.path.join(self.BASE_DIR, 'data', 'KEN_ALL.CSV'),
            'connection': self.connection
        }
        redis_tbar.load_data_into_redis(**init)

    def test_load_data(self):
        """
        Test normal upload using DirectoryFlickrUpload
        TODO: Check file private/non-family status
        :return:
        """

        loaded_data = redis_tbar.RedisYuubinBango.load(connection=self.connection, postal_code='1640001')
        self.assertEqual(loaded_data.code, u'1640001')
        self.assertEqual(loaded_data.old_code, u'164')
        self.assertEqual(loaded_data.pref, u'\u6771\u4eac\u90fd')
        self.assertEqual(loaded_data.city, u'\u4e2d\u91ce\u533a')
