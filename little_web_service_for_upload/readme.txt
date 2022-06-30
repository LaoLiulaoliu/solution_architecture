#### first web server for download

> * busybox httpd -c site.conf -p 8080 -f

access http://127.0.0.1:8080/msg.txt, input username and password(in site.conf LiLei and ILoveHanMeimei)


#### second web server for upload

> * socat TCP4-LISTEN:5555,reuseaddr,fork EXEC:./http_pip.py

upload multiple files to this server.


采用面向对象的思维或以类型驱动开发的思维,
体现对应范式的设计原则同时不过度设计,
覆盖各种正常和异常路径,
包含良好的自动化构建和自动化测试.
