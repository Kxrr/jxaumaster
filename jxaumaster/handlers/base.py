# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import base64
import pickle

from jxaumaster.config.settings import COOKIES_NAME
from jxaumaster.data.r_models import db_session, Session

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    ret = None

    def prepare(self):
        self.set_header('Content-Type'.encode('utf-8'), 'application/json')
        self.ret = {'uuid': str(uuid.uuid4()), 'status': True}

    def produce(self, **kwargs):
        for k, v in kwargs.items():
            self.ret[k] = v

    def response(self):
        return self.write(self.ret)

    def get_current_user(self):
        session_key = self.get_secure_cookie(COOKIES_NAME)
        s = db_session()
        sessions = s.query(Session).filter_by(session_key=session_key)
        if sessions:
            session = sessions.one()
            if session.is_valid():
                user = session.get_decoded()
                return user
        return None

    @classmethod
    def dumps(cls, data):
        data = pickle.dumps(data)[::-1]
        return base64.b64encode(data)

    @classmethod
    def loads(cls, string):
        data = base64.b64decode(string)
        return pickle.loads(data[::-1])


if __name__ == '__main__':
    pass
