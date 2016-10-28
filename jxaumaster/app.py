# -*- coding: utf-8 -*-
import tornado.web
import tornado.gen
import tornado.options
import tornado.ioloop

from jxaumaster.handlers.base import BaseHandler
from jxaumaster.handlers.query import StudentQueryHandler, GradeQueryHandler, ExamQueryHandler
from jxaumaster.handlers.auth import LoginHandler, LogoutHandler, ValidateHandler, FreshHandler

tornado.options.define("port", default=8888, help="run on the given port", type=int)


class MainHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write('hello')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', MainHandler),
            ('/login', LoginHandler),
            ('/logout', LogoutHandler),
            ('/fresh_login', FreshHandler),
            ('/validate', ValidateHandler),
            ('/students?', StudentQueryHandler),
            ('/student/grade?', GradeQueryHandler),
            ('/student/exam?', ExamQueryHandler),
        ]

        settings = {
            'cookie_secret': b'(\xd0aZ\x87\x0f\x9f\x8c\x95Y0JbD\x12\x8c',
            'login_url': '/login',
        }

        super(Application, self).__init__(handlers=handlers, **settings)


def make_app():
    return Application()


def main():
    tornado.options.parse_command_line()
    application = make_app()
    application.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
