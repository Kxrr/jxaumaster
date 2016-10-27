# -*- coding: utf-8 -*-
from jxaumaster.utils.funtional import encode, loads
from jxaumaster.tests import AsyncHTTPTestCase


class TestLogin(AsyncHTTPTestCase):
    def test_login_success(self):
        # TODO mock success
        data = self._login({'username': '20140000', 'password': 'should_be_right'})
        self.assertTrue(data['status'])

        user = data.get('user')
        self.assertTrue(user)
        self.assertIsNotNone(user['name'])
        self.assertIsNotNone(user['username'])

    def test_login_fail(self):
        data = self._login({'username': '20120000', 'password': '000000'})
        self.assertFalse(data['status'])

    def _login(self, data):
        rsp = self.fetch('/login', method='POST', body=encode(data))
        return loads(rsp.body)
