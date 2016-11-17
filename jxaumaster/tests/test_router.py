# -*- coding: utf-8 -*-
from mock import patch

from jxaumaster.tests import AsyncHTTPTestCase


class TestRouter(AsyncHTTPTestCase):
    def test_404_error(self):
        data = self.get('/not_exist_path')
        self.assert_response_failure(data)
        error = data.get('error')
        self.assertIsInstance(error, dict)
        self.assertEqual(error['code'], 404)

    def test_500_error(self):
        pass
