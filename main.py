#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pycharm不支持getpass
import os
import operator
import hashlib
import sql
from base.common import sql_input, string_to_token
import base.default_variable as dv
import time
import sys
from tools.log import save_log
from multiprocessing import Process, Queue


# 验证用户登录
def login(username, password):
    password = hashlib.new('md5', password.encode('utf-8')).hexdigest()
    with open(dv.PROJECT_PATH + r'/user/user_pwd.txt', 'r') as f:
        for line in f.readlines():
            user = (line.strip().split('#')[0], line.strip().split('#')[1])
            if line.split('#')[2].strip('\n') == 'admin':
                dv.DATABASE_ADMIN.append(line.strip().split('#')[0])
            if operator.eq(user, (username, password)):
                return True
    return False

def sql_interface(input_string):
    input_string = input_string.lower()
    token = string_to_token(input_string)
    if token[0] == 'exit':
        print("Bye ! ! !")
        print('---------------------')
        return -1
    elif token[0] == 'use':
        dv.CURRENT_DB = token[1]
    elif token[0] == 'help':
        sql.helps.parse(token)
    elif token[0] == 'create':
        sql.create.parse(token, input_string)
    elif token[0] == 'select':
        sql.select.parse(token)
    elif token[0] == 'insert':
        sql.insert.parse(input_string)
    elif token[0] == 'delete':
        sql.delete.parse(input_string)
    elif token[0] == 'update':
        sql.update.parse(input_string)
    elif token[0] == 'grant':
        sql.grant.parse(input_string)
    elif token[0] == 'revoke':
        sql.revoke.parse(input_string)
    else:
        print('未知的SQL语句')


def main():
    log_info = Queue()
    print("请输入用户名和密码!!!")
    username = input("username: ")
    password = getpass.getpass("password: ")
    # username = 'root'
    # password = 'root'

    process_log = Process(target=save_log, args=(log_info,))
    process_log.start()

    if login(username, password):
        dv.CURRENT_USER = username
        os.system('cls')
        if username in dv.DATABASE_ADMIN:
            print("Hello ADMIN %s" % dv.CURRENT_USER)
        else:
            print("Hello USER %s" % dv.CURRENT_USER)
        log_info.put("[%s]%s login" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), dv.CURRENT_USER))
        print(r"""
                ------------------------------------- 
               |    S   u   r   p   r   i   s   e    |
                ------------------------------------- 
               |                                     |
               |   ------     -------      |         |
               |  |          |       |     |         |
               |  |          |       |     |         |
               |   ------    |       |     |         |
               |         |   |       |     |         |
               |         |    ------\      |         |
               |   ------            \      -------  |
               |                                     |                        
                ------------------------------------- 
         """)

        while True:
            input_string = sql_input()
            log_info.put("[%s]%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), input_string))
            if sql_interface(input_string) == -1:
                log_info.put("[%s]%s logout" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), dv.CURRENT_USER))
                break
    else:
        print("用户名或密码错误！！请重试.....")


if __name__ == '__main__':
    main()
