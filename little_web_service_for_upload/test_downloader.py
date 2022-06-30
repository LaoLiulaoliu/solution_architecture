#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from urllib.parse import urljoin
from urllib.error import HTTPError
from downloader import Downloader


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.site_url = "http://127.0.0.1:8080"
        self.msg_url = urljoin(self.site_url, "msg.txt")
        self.username = "LiLei"
        self.password = "ILoveHanMeime"

    def prepare_password(self, username, password):
        self.downloader = Downloader(self.site_url, username, password)
        handler = self.downloader.create_password_manager()
        self.downloader.install_opener(handler)

    def test_normal(self):
        self.prepare_password(self.username, self.password)
        data = self.downloader.down(self.msg_url)
        if data is not None:
            self.assertEqual(data, "We all know it!")

    def test_wrong_password(self):
        self.prepare_password(self.username, "password")
        try:
            data = self.downloader.down(self.msg_url)
        except HTTPError as e:
            self.assertEqual(e.code, 401)

    def test_wrong_url(self):
        self.prepare_password(self.username, self.password)
        try:
            data = self.downloader.down(urljoin(self.site_url, "wrong"))
        except HTTPError as e:
            self.assertEqual(e.code, 404)


if __name__ == "__main__":
    unittest.main()
