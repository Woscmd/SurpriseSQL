#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from disk.rwfile import write_to_txt
import base.default_variable as dv
from threading import Thread
import time
from disk.rwfile import write_to_log_txt


# 保存日志文件
def save_log(log):
    path = r'%s\log\log%s.txt' % (dv.PROJECT_PATH, time.strftime("%Y%m%d", time.localtime()))
    with open(path, 'w') as f:
        for i in range(3):
            t = Thread(target=write_to_log_txt, args=(f, log))
            t.start()


if __name__ == "__main__":
    print(time.strftime("%Y%m%d", time.localtime()))
