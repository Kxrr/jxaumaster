# -*- coding: utf-8 -*-
from jxaumaster.handlers.base import BaseHandler
from jxaumaster.data.models import Student


class StudentQueryHandler(BaseHandler):
    """
    TODO: __contains...支持, 添加动态参数(phone_url)
    """
    AVAILABLE_FIELDS = ('sid', 'name')

    def get(self, *args, **kwargs):
        query = self.get_query_args()
        field_filter = self.get_argument('only', '', strip=True).split(',')
        photo = self.get_argument('photo', False)

        students = self.query_students(query, field_filter)

        if photo:
            self.attach_phone_link(students)

        self.produce(students=students)
        self.response()

    def attach_phone_link(self, students):
        for student in students:
            student['phone_link'] = 'http://prefix/{}'.format(student['sid'])
        return students

    def query_students(self, query, field_filter):
        """
        :rtype: dict
        """
        students = Student.query(**query)
        if any(field_filter):
            students = students.only(*field_filter)

        return Student.to_python(students)

    def get_query_args(self):
        query = {}
        args = self.get_argument('q', strip=True, default='').split(',')
        for arg in args:
            arg = arg.strip()
            k, v = arg.split('=')
            if k in self.AVAILABLE_FIELDS:
                query[k] = v
        return query
