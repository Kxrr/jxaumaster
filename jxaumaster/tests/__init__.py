# -*- coding: utf-8 -*-
import tornado.testing

from jxaumaster.app import Application
from jxaumaster.utils.funtional import loads, encode


class AsyncHTTPTestCase(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return Application()

    def get(self, path):
        rsp = self.fetch(path, method='GET')
        return loads(rsp.body)

    def post(self, path, data):
        rsp = self.fetch(path, method='POST', body=encode(data))
        return loads(rsp.body)

    @staticmethod
    def has_error(data):
        return bool(data.get('error', None))

    def assert_response_success(self, data):
        """
        :type data: dict
        """
        return self.assertFalse(self.has_error(data))

    def assert_response_failure(self, data):
        return self.assertTrue(self.has_error(data))
