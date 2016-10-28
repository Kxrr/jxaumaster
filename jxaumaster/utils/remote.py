# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import inspect
import functools
import re
from urlparse import urljoin

from tornado import gen
from tornado import escape
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse

from jxaumaster.utils.object import AttributeDict, Mapper
from jxaumaster.utils.funtional import encode, loads, dumps


def re_login(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        kw = inspect.getcallargs(method, *args, **kwargs)
        user = kw.get('user')
        if user:
            pass
        else:
            return method(**kwargs)

    return wrapper


class User(AttributeDict):
    version = 0.1

    def __init__(self, guid=None, username=None, password=None, name=None, **kwargs):
        self.name = name
        self.guid = guid
        self.username = username
        self.password = password

        super(User, self).__init__(**kwargs)


class JxauUtils(object):
    HEADERS = {
        'Host': 'jwgl.jxau.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/10.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Referer': 'http://jwgl.jxau.edu.cn/user/login',
        'Connection': 'keep-alive'
    }

    GRADE_NAME_MAP = {
        'Kcmc': 'class_name',
        'Xm': 'student_name',
        'Xq': 'term',
        'Kclb': 'class_category',
        'Zpcj': 'grade',
    }

    EXAM_NAME_MAP = {
        'Kcmc': 'class_name',
        'Xq': 'term',
        'Khfs': 'type',
        'KsSj': 'time',
        'Ksdd': 'room',
    }

    LOGIN_URL = 'http://jwgl.jxau.edu.cn/User/CheckLogin'
    SCHEDULE_URL = 'http://jwgl.jxau.edu.cn/Content/Reporters/Keibao/ViewKebiao.aspx?kbtype=xh&xq=20161&usercode={sid}'
    GRADE_URL = 'http://jwgl.jxau.edu.cn/SystemManage/CJManage/GetXsCjByXh/{guid}'
    EXAM_URL = 'http://jwgl.jxau.edu.cn/PaiKaoManage/KaoShiAnPaiChaXunManage/GetKaoShiInfo_Student/{guid}'
    INDEX_URL = 'http://jwgl.jxau.edu.cn/Main/Index/{guid}'

    @classmethod
    def _get_headers_with_cookies(cls, cookies):
        cookies = cookies or ''
        headers = cls.HEADERS.copy()
        headers.update({'Cookie': cookies})
        return headers

    @classmethod
    @gen.coroutine
    def get_name(cls, sid):
        """姓名"""
        pattern = re.compile('第.学期(.*?)\(')
        rsp = yield AsyncHTTPClient().fetch(cls.SCHEDULE_URL.format(sid=sid))
        m = pattern.search(rsp.body.decode('utf-8'))

        if m:
            raise gen.Return(m.group(1))
        raise gen.Return('')

    @classmethod
    @gen.coroutine
    def _login(cls, post_data):
        """向学校服务器发送登录请求"""
        # http://www.tornadoweb.org/en/stable/httpclient.html#tornado.httpclient.AsyncHTTPClient
        rsp = yield AsyncHTTPClient().fetch(
            HTTPRequest(
                url=cls.LOGIN_URL,
                method='POST',
                body=encode(post_data),
                headers=cls.HEADERS,
                follow_redirects=False,
            ),
            raise_error=False,
        )
        raise gen.Return(rsp)

    @classmethod
    @gen.coroutine
    def login(cls, username, password):
        post_data = {
            'UserName': username,
            'PassWord': password,
            'validation': '',
        }

        rsp = yield cls._login(post_data)

        def login_success(code, url):
            return (code in [200, 302]) and ('用户名或密码错误' not in url)

        loc = ' '.join(rsp.headers.get_list('Location'))
        next_url = urljoin(cls.LOGIN_URL, loc)

        if login_success(rsp.code, escape.to_unicode(escape.url_unescape(next_url))):
            user = User()
            user.cookies = '; '.join(rsp.headers.get_list('Set-Cookie'))
            user.guid = next_url[35:]
            user.username = username
            user.password = password
            user.name = yield cls.get_name(sid=username)
            raise gen.Return(user)
        raise gen.Return(None)

    @classmethod
    def _fetch(cls, cookies, url, request_kw=None, fetch_kw=None):
        """
        :type cookies: basestring
        :type url: unicode | basestring
        :type request_kw: dict
        :type fetch_kw: dict
        :rtype: HTTPResponse
        """
        request_kw = request_kw or {}
        fetch_kw = fetch_kw or {}

        request = HTTPRequest(url=url, headers=cls._get_headers_with_cookies(cookies), **request_kw)
        return AsyncHTTPClient().fetch(request, **fetch_kw)

    @classmethod
    def _map(cls, raw_list, name_map):
        """
        :type raw_list: list[dict]
        :type name_map: dict
        """
        return [Mapper(raw, name_map) for raw in raw_list]

    @classmethod
    def _term_filter(cls, term, _list):
        return filter(lambda d: d.get('term') == str(term), _list)

    @classmethod
    @gen.coroutine
    def get_grade(cls, user, term):
        """成绩"""
        url = cls.GRADE_URL.format(guid=user.guid)
        rsp = yield cls._fetch(cookies=user.cookies, url=url, request_kw={'method': 'POST', 'body': encode({})})

        raw_grades = loads(rsp.body).get('Data')
        grades = cls._map(raw_grades, cls.GRADE_NAME_MAP)
        filtered_grades = cls._term_filter(term, grades)
        raise gen.Return(filtered_grades)

    @classmethod
    @gen.coroutine
    def get_exam_time(cls, user, term):
        """考试安排"""
        p = {
            'Xq': term,
            'limit': '100',
            'start': '0'
        }
        url = cls.EXAM_URL.format(guid=user.guid)
        rsp = yield cls._fetch(cookies=user.cookies, url=url, request_kw={'method': 'POST', 'body': encode(p)})

        raw_exams = loads(rsp.body).get('Data')
        exams = cls._map(raw_exams, cls.EXAM_NAME_MAP)
        filtered_schedules = cls._term_filter(term, exams)
        raise gen.Return(filtered_schedules)

    def undo(self):
        pass
        # def post_advice(self):
        #     self.data_advice = {
        #         "content": "Jxau.ga " + str(strftime('%Y%m%d')) + " Advice\n" + self.advice_content
        #     }
        #     self.exam_response_advice = requests.post('http://push.kxrr.us/write_email', data=self.data_advice).content

        # def get_rate_list(self):
        #     url = 'http://jwgl.jxau.edu.cn/Views/Xscp/GetCpnrForXs' + self.guid
        #     rate_list = list()
        #     for term in ('20151', '20152'):
        #         data = dict(start='0', limit='30', xq=term)
        #         rsp = self.s.post(url=url, data=data)
        #         if rsp:
        #             rate_list += rsp.json().get('Data')
        #     return rate_list

        # def start_rate(self, info_data):
        #     url = 'http://jwgl.jxau.edu.cn/JxcpManage/Xscp/Savefen' + self.guid
        #     result = 0
        #     for i in info_data:
        #         data = dict(
        #             ids='1,2,3,4,5,6,7,8,9,10,',
        #             fens='5,5,5,5,5,5,5,5,5,5,',
        #             jxbbh=i.get('Jxbbhs'),
        #             pingyu='nice!',
        #             jsbh=i.get('Jsbh'),
        #         )
        #         rsp = self.s.post(url=url, data=data)
        #         if rsp:
        #             if rsp.json().get('success'):
        #                 result += 1
        #     return result
        #
        # @property
        # def index_url(self):
        #     return 'http://jwgl.jxau.edu.cn/Main/Index/{}'.format(self.guid)
        #
        # def update_session(self, cookies, guid):
        #     """设定post请求的cookies"""
        #     self.s.post = lambda **kwargs: requests.post(cookies=cookies, **kwargs)
        #     self.s.get = lambda **kwargs: requests.get(cookies=cookies, **kwargs)
        #     self.guid = guid


if __name__ == '__main__':
    pass
