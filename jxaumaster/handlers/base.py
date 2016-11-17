# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import base64
import pickle

from jxaumaster.config.settings import COOKIES_NAME
from jxaumaster.data.r_models import db_session, Session

import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        self.ret = {}
        self.request_id = str(uuid.uuid4())

        super(BaseHandler, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.write_error(404)

    def prepare(self):
        self.set_header('Content-Type'.encode('utf-8'), 'application/json')

    def produce(self, **kwargs):
        for k, v in kwargs.items():
            self.ret[k] = v

    def response(self):
        return self.write(self.ret)

    def get_current_user(self):
        session_key = self.get_secure_cookie(COOKIES_NAME)
        s = db_session()
        session = s.query(Session).filter_by(session_key=session_key).first()
        if session:
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

    def write_error(self, status_code, **kwargs):
        error = {
            'message': '',
            # 'type': str(e.__class__.__name__),
            'code': status_code,
            'trace_id': self.request_id,
        }
        self.produce(error=error)
        return self.response()

if __name__ == '__main__':
    pass
