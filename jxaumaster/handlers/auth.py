# -*- coding: utf-8 -*-
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler

from jxaumaster.handlers.base import BaseHandler
from jxaumaster.utils.remote import JxauUtils


# https://github.com/bdarnell/async_dropbox/blob/master/demo/main.py
# 看flask实现的login


class LoginHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        result = yield JxauUtils.login(username, password)
        if result.guid:
            self.set_secure_cookie('session', self.dumps(result))
            self.produce(user={'name': result.name, 'username': result.username})
        else:
            self.produce()
        self.response()


class LogoutHandler(RequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        data = yield JxauUtils.fetch('aaa',
                                     'http://jwgl.jxau.edu.cn/Content/Reporters/Keibao/ViewKebiao.aspx?kbtype=xh&xq=20161&usercode=20142961')
        self.write(data.body)
