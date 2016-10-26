# -*- coding: utf-8 -*-
from jxaumaster.handlers.base import BaseHandler
from jxaumaster.data.models import Student


class StudentQueryHandler(BaseHandler):
    """
    TODO: __contains...支持, 添加动态参数(phone_url)
    """

    def get(self, *args, **kwargs):
        q = self.get_argument('q', strip=True, default='').split(',')
        field_filter = self.get_argument('only', '', strip=True).split(',')
        photo = self.get_argument('photo', False)

        students = StudentQuery(Builder(q)).query(field_filter)

        if photo:
            self.attach_phone_link(students)

        self.produce(students=students)
        self.response()

    def attach_phone_link(self, students):
        for student in students:
            student['phone_link'] = 'http://prefix/{}'.format(student['sid'])
        return students


class Builder(object):
    """
    配置Document.objects所需的参数
    """
    AVAILABLE_FIELDS = ('sid', 'name')
    CUSTOM_FIELDS = ('hometown',)

    def __init__(self, query_list):
        """
        :type query_list: dict
        """
        self.query_kw = dict(map(lambda s: s.split('='), query_list))

    def build(self):
        query = {}
        query.update(self.build_custom_kw())
        query.update(self.build_mongo_kw())
        return query

    def build_mongo_kw(self):
        _q = {}
        for k, v in self.query_kw.copy().items():
            if k in self.AVAILABLE_FIELDS:
                _q[k] = v
                self.query_kw.pop(k, None)  # 这里处理过后续就不需要处理了
        return _q

    def build_custom_kw(self):
        """
        :return:
        """
        _q = {}
        hometown = self.query_kw.pop('hometown', None)
        if hometown:
            _q['hometown'] = self.fix_hometown(hometown)
        return _q

    def fix_hometown(self, ht):
        return ht


class Query(object):
    """
    执行查询并做一些后续工作, 比如only
    """

    def __init__(self, builder):
        self.builder = builder


class StudentQuery(Query):
    DEFAULT_EXCLUDES = {'id', }

    def query(self, field_filter):
        """
        :rtype: dict
        """
        objects_kw = self.builder.build()
        students = Student.objects(**objects_kw).exclude(*self.DEFAULT_EXCLUDES)

        if any(field_filter):
            students = students.only(*field_filter)

        return Student.to_python(students)
