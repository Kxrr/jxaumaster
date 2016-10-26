# -*- coding: utf-8 -*-
import asyncmongo
import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        # return self.application.db
        return


