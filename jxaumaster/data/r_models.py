# -*- coding: utf-8 -*-
import pickle
import base64
import datetime
import uuid

from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Session(Base):
    __tablename__ = 'session'
    session_key = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_data = Column(String)
    expire_date = Column(DateTime)

    def get_decoded(self):
        return self.loads(self.session_data)

    def is_valid(self):
        return datetime.datetime.now() < self.expire_date

    @classmethod
    def store(cls, data, expire_in=30):
        return cls(session_data=cls.dumps(data),
                   expire_date=datetime.datetime.now() + datetime.timedelta(days=expire_in))

    @classmethod
    def dumps(cls, data):
        data = pickle.dumps(data)[::-1]
        return base64.b64encode(data)

    @classmethod
    def loads(cls, string):
        data = base64.b64decode(string)
        return pickle.loads(data[::-1])


engine = create_engine('sqlite:///orm_in_detail2.sqlite')

db_session = sessionmaker()
db_session.configure(bind=engine)
Base.metadata.create_all(engine)
