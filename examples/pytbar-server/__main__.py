import logging

import tornado.options
import tornado.ioloop
import tornado.web

from tornado_tbar import *

__author__ = 'jawaad'

# Run the Tornado server if this is run directly.
if __name__ == "__main__":
    tornado.options.define("port", default=8887, help="run on the given port", type=int)
    tornado.options.parse_config_file("server.conf")
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/", YuubinJsonServer),
    ])

    logging.info("starting postal code web server on port %d" % tornado.options.options['port'].value())
    application.listen(int(tornado.options.options['port'].value()))
    tornado.ioloop.IOLoop.instance().start()
