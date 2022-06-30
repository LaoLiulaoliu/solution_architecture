#!/usr/bin/env python3
# usage: socat TCP4-LISTEN:5555,reuseaddr,fork EXEC:./http.py

import os
import sys
from traceback import format_exc
from log import logging_stream_file

logger = logging_stream_file('.', 'pai-log.log')
path = './upfile/'
if not os.path.exists(path):
    os.makedirs(path)

print("""HTTP/1.0 200
Connection: close
Content-Type: text/plain
Content-Length: 8

I GOT IT""")
sys.stdout.flush()


GLOBALS = {
    "BOUNDRY": "-------------",
    "KEY": "X-KEY: PAI-PUZZLE",
    "STATE": "HEADER", # or "FORM", "DATA"
    "AUTH": False,
}

def get_content():
    data = []

    try:
        contents = sys.stdin.readlines()

        for line in contents:
            if GLOBALS["STATE"] == "HEADER":
                if line.startswith(GLOBALS["KEY"]): GLOBALS["AUTH"] = True
                if line.find("boundary=") > 0: GLOBALS["BOUNDRY"] = line[line.find("boundary=") + 9:].rstrip()
            if line.find(GLOBALS["BOUNDRY"]) > -1:
                if not GLOBALS["AUTH"]: break
                if GLOBALS["STATE"] == "HEADER": GLOBALS["STATE"] = "FORM"
                if GLOBALS["STATE"] == "DATA": GLOBALS["STATE"] = "FORM"
            if line.strip() == "" and GLOBALS["STATE"] == "FORM":
                GLOBALS["STATE"] = "DATA"
                continue
            if GLOBALS["STATE"] == "DATA":
                if line.find("FILENAME:") > -1:
                    filename = line[line.find("FILENAME:") + 9:].strip()
                    with open(os.path.join(path, filename), "w") as fd:
                        fd.write("".join(data))
                    data = []
                else:
                    data.append(line)
    except Exception as e:
        logger.info(format_exc())

    GLOBALS["BOUNDRY"] = "-------------"
    GLOBALS["STATE"] = "HEADER"
    GLOBALS["AUTH"] = False

    return data


if __name__ == "__main__":
    data = get_content()
    if data:
        with open(os.path.join(path,"pai.txt"), "w") as fd:
            fd.write("".join(data))
