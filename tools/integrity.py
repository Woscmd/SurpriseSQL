#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base.default_variable as dv
import disk.rwfile as rwfile
from base.path import *
import re


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
                    return False
            else:
                return False
    return True
