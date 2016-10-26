# -*- coding: utf-8 -*-
# https://github.com/bitly/asyncmongo
# https://github.com/nellessen/Real-Time-Web-App-Stack-with-Python-Tornado/blob/master/chat-asyncmongo-longpolling/app.py
import asyncmongo

import tornado.web
import tornado.gen
import tornado.options
import tornado.ioloop

from jxaumaster.base import BaseHandler

tornado.options.define("port", default=8888, help="run on the given port", type=int)


class MainHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', MainHandler),
        ]

        settings = {
            'cookie_secret': b'(\xd0aZ\x87\x0f\x9f\x8c\x95Y0JbD\x12\x8c',
        }

        super(Application, self).__init__(handlers=handlers, **settings)


def main():
    tornado.options.parse_command_line()
    application = Application()
    application.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
