# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from tornado.web import authenticated
from tornado import gen

from jxaumaster.handlers.base import BaseHandler
from jxaumaster.data.models import Student
from jxaumaster.utils.remote import JxauUtils


class ExamQueryHandler(BaseHandler):
    """查询考试安排"""

    @authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        term = self.get_argument('term', default='20152')
        exams = yield JxauUtils.get_exam_time(user=self.current_user, term=term)
        self.produce(exams=exams)
        self.response()


class GradeQueryHandler(BaseHandler):
    """
    查询成绩
    """

    @authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        term = self.get_argument('term', default='20152')
        grades = yield JxauUtils.get_grade(user=self.current_user, term=term)
        self.produce(grades=grades)
        self.response()


class StudentQueryHandler(BaseHandler):
    """
    查询学生信息
    """

    def get(self, *args, **kwargs):
        q = self.get_argument('q', strip=True, default='').split(',')
        field_filter = self.get_argument('only', '', strip=True).split(',')
        photo = self.get_argument('photo', False)
        students = StudentQuery(QueryBuilder(q)).query(field_filter)
        if photo:
            self.attach_photo_url(students)
        self.produce(students=students)
        self.response()

    @staticmethod
    def attach_photo_url(students):
        for student in students:
            student['photo_url'] = 'http://prefix/{}'.format(student['sid'])
        return students


class QueryBuilder(object):
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
                self.query_kw.pop(k, None)  # 后续不需要处理
        return _q

    def build_custom_kw(self):
        _q = {}
        hometown = self.query_kw.pop('hometown', '')
        if hometown:
            _q['hometown__contains'] = self.fix_hometown(hometown)
        return _q

    @staticmethod
    def fix_hometown(text):
        WEIGHTS = {
            'prov': 30,
            'city': 25,
            'county': 20,
            'district': 15,
        }
        text = text.decode('utf-8') if not isinstance(text, unicode) else text
        pattern = re.compile(r'(?P<prov>.*省)?(?P<city>.*市)?(?P<county>.*县)?(?P<district>.*区)?')
        m = pattern.search(text)
        if m:
            d = m.groupdict()
            box = {WEIGHTS[k]: v for k, v in d.items() if v}
            if box:
                return box[min(box.keys())].strip()
        return text


class StudentQuery(object):
    """
    执行查询并做一些后续工作, 比如only
    """
    DEFAULT_EXCLUDES = {'id', 'birthday'}

    def __init__(self, builder):
        self.builder = builder

    def query(self, field_filter):
        """
        :rtype: dict
        """
        objects_kw = self.builder.build()
        students = Student.objects(**objects_kw).exclude(*self.DEFAULT_EXCLUDES).limit(100)

        if any(field_filter):
            students = students.only(*field_filter)

        return Student.to_python(students)
