# -*- coding: utf-8 -*-
import urllib
import json


def encode(d):
    """
    :type d: dict
    """
    return urllib.urlencode(d)


def loads(j):
    return json.loads(j)


def dumps(d, **kwargs):
    return json.dumps(d, ensure_ascii=False, **kwargs)
