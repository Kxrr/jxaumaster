# -*- coding: utf-8 -*-
import unittest
from jxaumaster.utils.remote import User


class TestUser(unittest.TestCase):
    data = {
        'username': '20141234',
        'password': '000000',
        'guid': '77ade96d-6f20-49e8-90da-c9ffb8cc02e4',
        'name': '小明',
        'cookies': 'ASP.NET_SessionId=ywkcl5jhraqvzbzs442ciwqw; '
    }

    def test_init(self):
        User(guid='', username='', password='', name='')

    def test_to_dict(self):
        user = User(**self.data)
        self.assertDictEqual(user, self.data)
