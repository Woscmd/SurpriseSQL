#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import disk.rwfile as rwfile
import numpy as np
from base.path import *
import base.default_variable as dv

def sql_input(prompt=' >', white_split=';'):
    print(dv.CURRENT_USER + '@' + dv.CURRENT_DB + prompt, end="")
    s = input()
    input_string = '%s' % s
    while len(s) == 0 or s[-1] not in white_split:
        s = input()
        input_string += '%s' % s
    return input_string

def string_to_token(input_string):
    input_string = input_string.strip()
    input_string = input_string.rstrip(';')
    input_string = input_string.replace(',', ' ')
    token = input_string.split(' ')
    return token

# 获取所有的用户名
def get_all_user():
    users = []
    user_pwd_path = dv.PROJECT_PATH + r'\user\user_pwd.txt'
    with open(user_pwd_path, 'r') as f:
        for line in f.readlines():
            users.append(line.split('#')[0])
    return users

# 获取用户对数据库db_name的权限
def get_user_permissions(username, db_name):
    permissions_path = get_permission_path()
    data = rwfile.read_from_csv(permissions_path)
    permission = []
    for item in data:
        if item[0] == username and (item[1] == db_name or item[1] == '*'):
            permission.append(item)
    return permission


def get_column_index(data, column):
    for row in data:
        for index in range(0, len(row)):
            if row[index] == column:
                return index

def get_row_index(data, row_name):
    for index in range(1, len(data)):
        if data[index][0] == row_name:
            return index

# 数据形式转化
def dataFrame_to_list(df):
    df_list = np.array(df)
    df_list = df_list.tolist()
    return list(df_list)

# 获取某个表定义时所有的列
def get_all_columns(table_name):
    columns = []
    path = get_table_info_path(dv.CURRENT_DB, table_name)
    data = rwfile.read_from_csv(path)
    for item in data:
        if item[0] == 'key':
            continue
        columns.append(item[0])
    return columns

def is_table(table_name):
    path = get_database_path(dv.CURRENT_DB)
    views_name = rwfile.read_from_txt(path + r'\views_name.txt')
    if table_name in views_name:
        return False
    else:
        return True

# 获取当前视图的定义
def get_view_definition(view_name):
    info_path = get_view_info_path(dv.CURRENT_DB, view_name)
    sql_value = rwfile.read_from_txt(info_path)
    tokens = string_to_token(sql_value[0])
    return tokens
