# -*- coding: utf-8 -*-


class AttributeDict(dict):

    def __getattribute__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        return super(AttributeDict, self).__setitem__(key, value)
