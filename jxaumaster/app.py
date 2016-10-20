# -*- coding: utf-8 -*-
# https://github.com/bitly/asyncmongo
# https://github.com/nellessen/Real-Time-Web-App-Stack-with-Python-Tornado/blob/master/chat-asyncmongo-longpolling/app.py
import asyncmongo

import tornado.web
import tornado.options
import tornado.ioloop

from jxaumaster.base import BaseHandler

tornado.options.define("port", default=8888, help="run on the given port", type=int)


class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.db.student2015.find({'Xm': '梁华'}, callback=self._on_response)

    def _on_response(self, response, error, *args, **kwargs):
        print


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', MainHandler),
        ]

        settings = {
            'cookie_secret': '9*&3kkcjjiapeiihpeirt',
        }

        super(Application, self).__init__(handlers=handlers, **settings)

        self.db = asyncmongo.Client(
            pool_id='default',
            host='127.0.0.1',
            port=27017,
            maxcached=10,
            dbname='jxau',
        )


def main():
    tornado.options.parse_command_line()
    application = Application()
    application.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
