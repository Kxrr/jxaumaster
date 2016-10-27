# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import pickle

import tornado.web
import uuid


class BaseHandler(tornado.web.RequestHandler):
    ret = None

    def prepare(self):
        self.set_header('Content-Type', 'application/json')
        self.ret = {'uuid': str(uuid.uuid4()), 'status': True}

    def produce(self, **kwargs):
        for k, v in kwargs.items():
            self.ret[k] = v

    def response(self):
        return self.write(self.ret)

    def get_current_user(self):
        user = self.get_secure_cookie('user')
        if user:
            user = self.loads(user)
            return user
        else:
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
