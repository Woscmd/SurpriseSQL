#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tools.default_variable as dv
import tools.rwfile as rwfile
import numpy as np
import re

# path

def get_database_path(database_name):
    return r'%s\%s' % (dv.DATA_PATH, database_name)

# table
def get_table_data_path(database_name, tb_name):
    return r'%s\%s\tables\%s_data.csv' % (dv.DATA_PATH, database_name, tb_name)

def get_table_info_path(database_name, tb_name):
    return r'%s\%s\tables\%s_info.csv' % (dv.DATA_PATH, database_name, tb_name)

# view
def get_view_data_path(database_name, view_name):
    return r'%s\%s\views\%s_data.csv' % (dv.DATA_PATH, database_name, view_name)

def get_view_info_path(database_name, view_name):
    return r'%s\%s\views\%s_info.txt' % (dv.DATA_PATH, database_name, view_name)

# index
def get_index_data_path(database_name, index_name):
    return r'%s\%s\indexes\%s_data.txt' % (dv.DATA_PATH, database_name, index_name)

def get_index_info_path(database_name, index_name):
    return r'%s\%s\indexes\%s_info.txt' % (dv.DATA_PATH, database_name, index_name)

def get_permission_path():
    return r'%s\user\permission.csv' % dv.PROJECT_PATH

def sql_input(prompt = ' >', white_split = ';'):
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

# 判断当前用户对当前数据库中某表是否拥有某个操作权限
def check_permission(table_name, permission):
    permission = permission.lower()
    permissions_path = get_permission_path()
    data = rwfile.read_from_csv(permissions_path)
    permissions = []
    for item in data:
        if item[0] == dv.CURRENT_USER and (item[1] == dv.CURRENT_DB or item[1] == '*') and (item[2] == 'table' or item[2] == '*') and (item[3] == table_name or item[3] == '*'):
            if item[4] == '*':
                permissions = ['insert', 'select', 'update', 'delete']
            else:
                permissions = item[4].split(',')
    if permission in permissions:
        return True
    else:
        return False

def get_column_index(data, column):
    for row in data:
        for index in range(0, len(row)):
            if row[index] == column:
                return index

def get_row_index(data, row_name):
    for index in range(1, len(data)):
        if data[index][0] == row_name:
            return index

# 非空约束检查
def check_not_null(table_name, column):
    path = get_table_info_path(dv.CURRENT_DB, table_name)
    data = rwfile.read_from_csv(path)
    row_index = get_row_index(data, column)
    column_num = len(data[0])
    for index in range(0, column_num):
        if data[row_index][index] == 'FALSE':
            print('未满足非空约束')
            return False
    return True

# 唯一约束检查
def check_unique(table_name, column, value):
    path = get_table_data_path(dv.CURRENT_DB, table_name)
    data = rwfile.read_from_csv(path)
    row_num = len(data)
    if row_num == 2:
        return True
    column_index = get_column_index(data, column)
    for index in range(1, row_num):
        if str(data[index][column_index]) == str(value):
            print('未满足唯一约束')
            return False
    return True

# check约束检查
def check_check(table_name, column, value):
    path = get_table_info_path(dv.CURRENT_DB, table_name)
    data = rwfile.read_from_csv(path)
    row_num = get_row_index(data, column)
    check_content = data[row_num][7]
    if value != check_content:
        return False
    return True

# 检查表约束条件
def check_constraint(table_name, cv):
    path = get_table_info_path(dv.CURRENT_DB, table_name)
    info = rwfile.read_from_csv(path)
    row_num = len(info)
    columns = cv.keys()
    for row in range(1, row_num):
        # 数据类型
        
        if info[row][0] in columns:
            # print(type(cv[info[row][0]]))
            if not (cv[info[row][0]].isdigit() and info[row][1].lower() == 'int'):
                print('数据类型不匹配')
                return False
            matchObj = re.search(r'varchar\(.*\)', info[row][1].lower())
            if matchObj:
                data_type = str
                if isinstance(cv[info[row][0]], data_type):
                    print('数据类型不匹配')
                    return False
            else:
                return True
        
        # 主键
        if info[row][2].lower() == 'true':
            if info[row][0].lower() in columns:
                if not check_unique(table_name, info[row][0], cv[info[row][0]]):
                    return False
            else:
                return False
        # 外键
        if info[row][3].lower() == 'true':
            if info[row][0].lower() in columns:
                if not check_unique(table_name, info[row][0], cv[info[row][0]]):
                    return False
            else:
                return False
        # 唯一
        if info[row][4].lower() == 'true':
            if not check_unique(table_name, info[row][0], cv[info[row][0]]):
                return False
        # 非空
        if info[row][5].lower() == 'true':
            if info[row][0].lower() not in columns:
                return False
        # 检查约束
        if info[row][7].lower() == 'true':
            if info[row][0].lower() in columns:
                if not check_check(table_name, info[row][0], cv[info[row][0]]):
                    return  False
            else:
                return False
    return True

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

if __name__ == '__main__':
    sql_string = 'SELECT Sname FROM Student WHERE Sno IN ( SELECT Sno FROM student WHERE sno = 109 );'

    tokens = string_to_token(sql_string.lower())
    print(tokens)
    l = ['106','111']
    print(type(l))