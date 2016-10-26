# -*- coding: utf-8 -*-
import tornado.web
import uuid


class BaseHandler(tornado.web.RequestHandler):
    ret = None

    def prepare(self):
        self.set_header("Content-Type", 'application/json')
        self.ret = {'uuid': str(uuid.uuid4())}

    def produce(self, **kwargs):
        for k, v in kwargs.items():
            self.ret[k] = v

    def response(self):
        return self.write(self.ret)

    def get_current_user(self):
        session_id = self.get_secure_cookie('session_id')
        user = {'session_id': session_id}
        return user
