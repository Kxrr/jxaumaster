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
    pass


if __name__ == '__main__':
    pass
