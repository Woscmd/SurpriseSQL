#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pycharm2018.2不支持getpass
import getpass
import operator
import hashlib
import sql
from tools.base import sql_input, string_to_token
import tools.default_variable as dv

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

def main():
    print("请输入用户名和密码!!!")
    username = input("username: ")
    password = getpass.getpass("password: ")
    #username = 'root'
    #password = 'root'
    if login(username, password):
        dv.CURRENT_USER = username
        print('---------------------------------')
        if username in dv.DATABASE_ADMIN:
            print("Hello ADMIN %s" % dv.CURRENT_USER)
        else:
            print("Hello USER %s" % dv.CURRENT_USER)
        print("Welcome to NewSQL .... ")
        print('---------------------------------')
        while True:
            input_string = sql_input()
            input_string = input_string.lower()
            token = string_to_token(input_string)
            if token[0] == 'exit':
                print("Bye ! ! !")
                print('---------------------')
                return
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
                sql.permission.grant(input_string)
            elif token[0] == 'revoke':
                sql.permission.revoke(input_string)
            else:
                print('未知的SQL语句')
    else:
        print("验证失败，请重试...")

if __name__ == '__main__':
    main()