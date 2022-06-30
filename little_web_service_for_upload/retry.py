#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from time import sleep


def retry(ExceptionToCheck, retries=3, delay=1, backoff=2):
    """Retry calling the decorated function using an exponential backoff.

    :param retries: number of times to retry before giving up
    :type retries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mretries, mdelay = retries, delay
            while mretries > 0:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    print(f"{e}, Retrying in {mdelay} seconds...")
                    sleep(mdelay)
                    mretries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


