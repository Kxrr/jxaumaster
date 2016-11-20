# -*- coding: utf-8 -*-
import tornado.web
import tornado.gen
import tornado.ioloop
from tornado.options import define, options

from jxaumaster.handlers.base import BaseHandler, BaseStaticFileHandler
from jxaumaster.handlers.query import StudentQueryHandler, GradeQueryHandler, ExamQueryHandler
from jxaumaster.handlers.auth import LoginHandler, LogoutHandler, ValidateHandler, FreshHandler
from jxaumaster.config import STATIC_ROOT, HTML_ROOT
from jxaumaster.utils.log import logger

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(BaseHandler):
    def prepare(self):
        pass

    def get(self, *args, **kwargs):
        return self.render('index.html')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', MainHandler),
            ('/login', LoginHandler),
            ('/logout', LogoutHandler),
            ('/fresh_login', FreshHandler),
            ('/validate', ValidateHandler),
            ('/search/student?', StudentQueryHandler),
            ('/student/grade?', GradeQueryHandler),
            ('/student/exam?', ExamQueryHandler),
            # ('/static/(.*)', BaseStaticFileHandler),
        ]

        settings = {
            'cookie_secret': b'(\xd0aZ\x87\x0f\x9f\x8c\x95Y0JbD\x12\x8c',
            'login_url': '/login',
            'static_path': STATIC_ROOT,
            'template_path': HTML_ROOT,
            'debug': True,
        }

        super(Application, self).__init__(handlers=handlers, **settings)


def make_app():
    return Application()


def main():
    options.parse_command_line()

    application = make_app()
    application.listen(options.port)
    logger.info('Running on http://127.0.0.1:{0}'.format(options.port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
