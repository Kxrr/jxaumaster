# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mongoengine import Document, connect
from mongoengine.fields import *

from jxaumaster.config.settings import MONGO_HOST, MONGO_PORT, MONGO_DBNAME

connect(db=MONGO_DBNAME, host=MONGO_HOST, port=MONGO_PORT)


class Student(Document):
    sid = StringField(db_field='Xh')
    name = StringField(db_field='Xm')
    classroom = StringField(db_field='Bjmc')
    hometown = StringField(db_field='Jg')
    sex = StringField(db_field='Xb')
    birthday = StringField(db_field='Csny')

    meta = {
        'collection': 'student_201610',
        'indexes': ['name', 'sid'],
        'index_background': True,
        'strict': False
    }

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'{0.name} {0.sid}'.format(self)


if __name__ == '__main__':
    pass
