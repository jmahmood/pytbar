py-tbar v0.3
============

Py-tbar is a library that parses Japan Posts' postal code CSV files and adds the parsed data to a DB.

The current library only supports Redis.

Dependencies:
- Python 2.7+
- redis-py

How To Use
------------
1. Get the CSV data (You can get it from http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip)

2. Load your data into Redis.  (Change variables into something that works for you)

        self.connection = redis.StrictRedis(port=6379, host='localhost')

        init = {
            'init_file': '/path/to/file.csv',
            'connection': self.connection
        }
        redis_tbar.load_data_into_redis(**init)

3. You can now query the data at any time by passing a redis instance and the postal code you want.

         loaded_data = redis_tbar.RedisYuubinBango.load(connection=redis.StrictRedis(port=6379, host='localhost'), postal_code='1640001')


Asides
-------------
〠 T-bar refers to the Japanese Post Office symbol (〒)

〠 My friend Paul MacMahon did something similar in Ruby: https://github.com/pwim/yubinbang

〠 We previously included a tornado server that handled this, but it is removed.  You can find it as part of py-tbar-server.

License
-------------
MIT License

Copyright (c) 2015 Jawaad Mahmood

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
