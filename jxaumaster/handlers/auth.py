# -*- coding: utf-8 -*-
from jxaumaster.handlers.base import BaseHandler
# https://github.com/bdarnell/async_dropbox/blob/master/demo/main.py
# 看flask实现的login


class LoginHandler(BaseHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        password = self.get_argument('username', '')

        if username and password:
            self.set_secure_cookie('session_id', '123')

        self.write('ok')


class LogoutHandler(BaseHandler):
    pass


