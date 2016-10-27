# -*- coding: utf-8 -*-
# https://github.com/bdarnell/async_dropbox/blob/master/demo/main.py
from tornado import gen
from tornado.web import authenticated

from jxaumaster.handlers.base import BaseHandler
from jxaumaster.utils.remote import JxauUtils


class LoginHandler(BaseHandler):
    def get(self):
        self.write('login here')

    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        user = yield JxauUtils.login(username, password)
        if user.guid:
            self.set_secure_cookie('user', self.dumps(user))
            self.produce(status=True, user={'name': user.name, 'username': user.username})
        else:
            self.produce(status=False)
        self.response()


class LogoutHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.set_secure_cookie('user', '')
        self.produce(status=True)
        self.response()


class ValidateHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.produce(status=True, user_session=dict(self.current_user))
        self.response()
