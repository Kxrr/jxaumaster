# -*- coding: utf-8 -*-
import unittest
from jxaumaster.handlers.base import BaseHandler
from jxaumaster.utils.remote import Session


class TestSerialize(unittest.TestCase):

    def setUp(self):
        self.data = {'name': '赵四'}
        self.data2 = {u'name': u'赵四'}

    def test_serialize(self):
        for data in (self.data, self.data2):
            dumped = BaseHandler.dumps(data)
            self.assertEqual(data, BaseHandler.loads(dumped))

    def test_serialize_session(self):
        session = Session(name='赵四')
        self.assertEqual(session, BaseHandler.loads(BaseHandler.dumps(session)))
