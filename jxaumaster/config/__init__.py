# -*- coding: utf-8 -*-
from os.path import dirname, abspath, join

PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))
STATIC_ROOT = join(PROJECT_ROOT, 'jxaumaster', 'static')
HTML_ROOT = join(STATIC_ROOT, 'html')
