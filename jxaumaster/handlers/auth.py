# -*- coding: utf-8 -*-
# https://github.com/bdarnell/async_dropbox/blob/master/demo/main.py
from tornado import gen
from tornado.web import authenticated

from jxaumaster.config.settings import COOKIES_NAME
from jxaumaster.data.r_models import db_session, Session
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
        self.set_user_cookie(user)
        self.response()

    def set_user_cookie(self, user):
        if user:
            session = Session.store(user)
            s = db_session()
            s.add(session)
            s.commit()
            self.set_secure_cookie(COOKIES_NAME, str(session.session_key))
            self.produce(user={'name': user.name, 'username': user.username, 'guid': user.guid})  # 登录成功后有guid
        else:
            self.produce(status=False)


class LogoutHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.set_secure_cookie(COOKIES_NAME, '')
        self.produce(status=True)
        self.response()


class ValidateHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.produce(user_session=dict(self.current_user))
        self.response()


class FreshHandler(LoginHandler):
    @authenticated
    @gen.coroutine
    def get(self):
        user = self.current_user
        new_user = yield JxauUtils.login(username=user.username, password=user.password)
        self.set_user_cookie(new_user)
        self.response()
