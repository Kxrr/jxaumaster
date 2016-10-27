# -*- coding: utf-8 -*-


class AttributeDictMixin(object):
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    def __getstate__(self):
        # http://stackoverflow.com/questions/2049849/why-cant-i-pickle-this-object
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)


class AttributeDict(dict, AttributeDictMixin):
    def __init__(self, **kwargs):
        super(AttributeDict, self).__init__(**kwargs)


class Mapper(object):
    def __new__(cls, *args):
        d, name_map = args
        assert isinstance(d, dict) and isinstance(name_map, dict)
        return {name_map[k]: v for k, v in d.items() if k in name_map}

    def __init__(self, d, named_map):
        pass


if __name__ == '__main__':
    d = {'name': 'Roy'}
    map = {'name': '名字'}

    print Mapper(d, map)
