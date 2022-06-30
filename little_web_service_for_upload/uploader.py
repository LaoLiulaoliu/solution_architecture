#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from uuid import uuid4
from io import BytesIO
import mimetypes
from urllib import request
from socket import setdefaulttimeout
from retry import retry


class Uploader(object):
    def __init__(self, site_url, timeout=10, retries=2):
        self.site_url = site_url
        setdefaulttimeout(timeout)

        self.files = []
        self.boundary = uuid4().hex.encode("utf-8")
        self.upload = retry(Exception, retries)(self.upload)

    def get_content_type(self):
        return "multipart/form-data"

    def add_file(self, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = (
            mimetypes.guess_type(filename)[0] or
            "application/octet-stream"
            )
        self.files.append((filename, mimetype, body))

    def upload(self, data):
        headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-type": self.get_content_type(),
            "Content-length": len(data)
        }

        req = request.Request(self.site_url, data=data, headers=headers)
        return request.urlopen(req).read().decode("utf-8")

    def __bytes__(self):
        """Return a byte-string representing the form data,
        including attached files.
        """
        buffer = BytesIO()
        auth = b"X-KEY: PAI-PUZZLE. boundary=" + self.boundary + b"\n"

        for filename, _, body in self.files:
            buffer.write(auth)
            buffer.write(b"\n")
            buffer.write(body + b"\n")
            buffer.write(b"FILENAME:" + filename.encode("utf-8") + b"\n")

        buffer.write(self.boundary + b"\n")
        return buffer.getvalue()


if __name__ == "__main__":
    site_url = "http://127.0.0.1:5555/"
    uploader = Uploader(site_url)

    uploader.add_file("pai-ai.txt", BytesIO(b"Machine Learning rocks."))
    uploader.add_file("pai-msg.txt", BytesIO(b"Python developer and blogger."))
    resp_data = uploader.upload(bytes(uploader))
    print(resp_data)


