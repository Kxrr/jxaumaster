# -*- coding: utf-8 -*-
import tornado.testing

from jxaumaster.app import Application


class AsyncHTTPTestCase(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return Application()
