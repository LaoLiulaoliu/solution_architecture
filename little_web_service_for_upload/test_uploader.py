#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
from io import BytesIO
from urllib.parse import urljoin
from urllib.error import HTTPError
from uploader import Uploader


class TestUploader(unittest.TestCase):
    def setUp(self):
        self.site_url = "http://127.0.0.1:5555"
        self.msg_url = urljoin(self.site_url, "msg.txt")

    def test_normal(self):
        uploader = Uploader(self.site_url)

        uploader.add_file("msg.txt", BytesIO(b"Python developer and blogger."))
        resp_data = uploader.upload(bytes(uploader))
        self.assertEqual("I GOT IT", resp_data)

    def test_wrong_port(self):
        uploader = Uploader(self.site_url[:-4] + "8888")

        uploader.add_file("msg.txt", BytesIO(b"Python developer and blogger."))
        try:
            resp_data = uploader.upload(bytes(uploader))
        except Exception as e:
            self.assertTrue("Connection refused" in str(e.reason))


if __name__ == "__main__":
    unittest.main()
