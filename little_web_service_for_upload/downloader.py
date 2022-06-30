#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request as request
from socket import setdefaulttimeout
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError
from retry import retry


class Downloader(object):
    def __init__(self, site_url, username, password, timeout=10, retries=2):
        self.site_url = site_url
        self.username = username
        self.password = password
        setdefaulttimeout(timeout)
        self.down = retry(Exception, retries)(self.down)

    def create_password_manager(self):
        password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.site_url, self.username, self.password)
        handler = request.HTTPBasicAuthHandler(password_mgr)
        return handler

    def install_opener(self, handler):
        opener = request.build_opener(handler)
        request.install_opener(opener)

    def down(self, url):
        r = request.urlopen(url)
        return r.read().decode("utf8")[:-1]


if __name__ == '__main__':
    site_url = "http://127.0.0.1:8080"
    msg_url = urljoin(site_url, "msg.txt")
    username = "LiLei"
    password = "ILoveHanMeime"

    downloader = Downloader(site_url, username, password)
    handler = downloader.create_password_manager()
    downloader.install_opener(handler)
    data = downloader.down(msg_url)
    if data is not None:
        print(f"Data: {data}|||")

