# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jxaumaster.tests import AsyncHTTPTestCase
from jxaumaster.handlers.query import QueryBuilder


class TestLocalQuery(AsyncHTTPTestCase):

    def test_fix_hometown(self):
        self.assertEqual('广州市', QueryBuilder.fix_hometown('广东省广州市'))
        self.assertEqual('天河区', QueryBuilder.fix_hometown('广东省广州市天河区'))
        self.assertEqual('南昌县', QueryBuilder.fix_hometown('南昌市 南昌县'))
