# -*- coding: utf-8 -*-
import os
import logging

from jxaumaster.config import PROJECT_ROOT

LOG_PATH = os.path.join(PROJECT_ROOT, 'jxaumaster', 'logs')
FORMAT = '[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d > %(message)s'
FORMATTER = logging.Formatter(FORMAT)


def config():
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

config()


def get_logger(name):
    _logger = logging.getLogger(name)
    file_handler = logging.FileHandler(filename=os.path.join(LOG_PATH, '{0}.log'.format(_logger.name)))
    file_handler.setFormatter(FORMATTER)

    if not _logger.handlers:
        _logger.addHandler(file_handler)

    return _logger


base_logger = logger = get_logger('jxaumaster')
handler_logger = get_logger('jxaumaster.handler')
auth_logger = get_logger('jxaumaster.handler.auth')
query_logger = get_logger('jxaumaster.handler.query')


if __name__ == '__main__':
    pass

