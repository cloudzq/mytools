# -*- coding:utf-8 -*-
"""
@Project:watchmen
@Language:Python3.6.4
@Author:Hans
@File:logtool.py
@Ide:PyCharm
@Time:2018/8/20 14:44
@Remark:
"""

import logging
from logging.handlers import TimedRotatingFileHandler


def log_init(logger, file_name):
    handler = TimedRotatingFileHandler(file_name, when='d', interval=1, backupCount=90)
    formatter = logging.Formatter('[%(asctime)]s [%(levelname)]s [%(funcname)]s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

logs = logging.getLogger()

if __name__ == '__main__':
    log_init(log,'/tmp/test.log')
    logs.info('test')