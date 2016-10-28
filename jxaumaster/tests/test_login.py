# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch, Mock
from tornado.concurrent import Future

from jxaumaster.utils.funtional import encode, loads
from jxaumaster.tests import AsyncHTTPTestCase
from jxaumaster.utils.remote import JxauUtils


class TestLogin(AsyncHTTPTestCase):
    @patch.object(JxauUtils, '_login')
    def test_login_success(self, _mock):
        mock_response = Mock()
        mock_response.return_value = Future()
        mock_response.code = 302
        mock_response.headers.get_list.side_effect = lambda key: \
            {
                'Location': ['/Main/Index/d9359cb0-f9a7-42c4-89d6-c2c05f5875dc'],
                'Set-Cookie': ['ASP.NET_SessionId=fwtqedargnx2ogfru0tsj544'],
            }.get(key)

        future = Future()
        future.set_result(mock_response)

        _mock.return_value = future

        data = self._post({'username': '20140000', 'password': 'should_be_right'})
        self.assertTrue(data['status'])

        user = data.get('user')
        self.assertTrue(user)
        self.assertIsNotNone(user['name'])
        self.assertEqual(user['username'], '20140000')

    def test_login_fail(self):
        data = self._post({'username': '20120000', 'password': '000000'})
        self.assertFalse(data['status'])

    def _post(self, data):
        rsp = self.fetch('/login', method='POST', body=encode(data))
        return loads(rsp.body)

    @patch.object(JxauUtils, '_login')
    def test_mock(self, mock_response):
        mock_response.code = 302
