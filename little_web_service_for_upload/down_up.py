#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import BytesIO
from urllib.parse import urljoin
from downloader import Downloader
from uploader import Uploader


def down():
    site_url = "http://127.0.0.1:8080"
    msg_url = urljoin(site_url, "msg.txt")
    username = "LiLei"
    password = "ILoveHanMeime"

    downloader = Downloader(site_url, username, password)
    handler = downloader.create_password_manager()
    downloader.install_opener(handler)
    return downloader.down(msg_url)

def upload(data):
    site_url = "http://127.0.0.1:5555/"
    uploader = Uploader(site_url)

    uploader.add_file("pai-ai.txt", BytesIO(b"Machine Learning rocks."))
    uploader.add_file("pai-msg.txt", BytesIO(data.encode("utf-8")))
    resp_data = uploader.upload(bytes(uploader))
    print(resp_data)


if __name__ == "__main__":
    data = down()
    upload(data)
