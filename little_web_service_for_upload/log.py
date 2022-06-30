#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import os
from logging.handlers import RotatingFileHandler


def logging_stream_file(path, name, maxBytes=1024 * 1024 * 50, backupCount=10, level='INFO'):
    if not os.path.exists(path):
        os.makedirs(path)

    basic_format = '%(asctime)s %(threadName)s %(filename)s:%(funcName)s %(lineno)-1d  %(levelname)-5s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(basic_format, date_format)

    logger = logging.getLogger()
    logger.setLevel(level)

    fhlr = RotatingFileHandler(filename=os.path.join(path, name), maxBytes=maxBytes, backupCount=backupCount)
    fhlr.suffix = "%Y-%m-%d.log"
    fhlr.setFormatter(formatter)
    logger.addHandler(fhlr)
    return logger

