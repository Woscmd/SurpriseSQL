#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import disk.rwfile as rwfile
import base.path as path
import base.default_variable as dv
from base.common import string_to_token

# 获取表约束
def get_key(key_item):
    k_list = []
    k_value = key_item.split(' ')[0]
    k_type = key_item.split(' ')[1]
    k_list.append(k_value)
    k_list.append(k_type)
    if 'primary key' in key_item:
        k_list.append('true')
    else:
        k_list.append('false')
    if 'foreign key' in key_item:
        k_list.append('true')
    else:
        k_list.append('false')
    if 'unique' in key_item:
        k_list.append('true')
    else:
        k_list.append('false')
    if 'not null' in key_item:
        k_list.append('true')
    else:
        k_list.append('false')
    if 'not null' not in key_item and 'null' in key_item:
        k_list.append('true')
    else:
        k_list.append('false')
    if 'check' in key_item:
        k_list.append('true')
    else:
        k_list.append('false')
    # print(k_list)
    return k_list

# 解析语句
def parse(token, sql):
    if token[1] == 'table':
        parse_table(sql)
    elif token[1] == 'view':
        parse_view(sql)
    elif token[1] == 'index':
        # parse_index(sql)
        pass
    else:
        print('语法错误')

# 解析create table语句并执行
def parse_table(sql):
    matchObj = re.search(r'^create table (.*) \(.*\);$', sql)
    if matchObj:
        table_name = matchObj.group(1)
        index = sql.find('(')
        # table_keys 字段及其定义
        table_keys = sql[index + 1:-2]
        table_keys = table_keys.split(',')
        info_path = path.get_table_info_path(dv.CURRENT_DB, table_name)
        data_path = path.get_table_data_path(dv.CURRENT_DB, table_name)
        db_path = path.get_database_path(dv.CURRENT_DB)
        # 检查该表是否存在
        if not os.path.exists(info_path):
            try:
                table_header = ['key', 'type', 'primary key', 'foreign key', 'unique', 'not null', 'null', 'check']
                # keys_list 存储table_header和所有字段的解析含义
                keys_list = list()
                label = []
                keys_list.append(table_header)
                for item in table_keys:
                    item.strip()
                    key_list = get_key(item)
                    label.append(key_list[0])
                    keys_list.append(key_list)
                rwfile.write_to_csv(info_path, keys_list)
                labels = list()
                labels.append(label)
                rwfile.write_to_csv(data_path, labels)
                # 将表名添加到tables_name.txt
                rwfile.write_to_txt(db_path + r'\tables_name.txt', table_name)
                print('CREATE TABLE ' + table_name + ' SUCCESSFUL')
            except Exception as e:
                print(e)
        else:
            print('TABLE ' + table_name + ' HAS EXIST')
    else:
        print('sql 语句格式错误')

# 解析create view语句并执行
def parse_view(sql):
    matchObj = re.search(r'^create view (.*) as (.*);$', sql)
    if matchObj:
        view_name = matchObj.group(1)
        child_select = matchObj.group(2)  # 子查询
        # 当前数据库绝对路径
        db_path = path.get_database_path(dv.CURRENT_DB)
        info_path = path.get_view_info_path(dv.CURRENT_DB, view_name)
        # 检查该视图是否存在
        if not os.path.exists(info_path):
            try:
                # 写入创建视图定义
                rwfile.write_to_txt(info_path, child_select)
                # 将视图名写入views_name.txt
                rwfile.write_to_txt(db_path + r'\views_name.txt', view_name)
                print('CREATE VIEW ' + view_name + ' SUCCESSFUL')
            except Exception as e:
                print(e)
        else:
            print('VIEW ' + view_name + ' HAS EXIST')
    else:
        print('sql 语句格式错误')

'''
def parse_index(sql):
    matchObj = re.search(r'^create index (.*) on (.*)\((.*)\);$', sql)
    if matchObj:
        index_name = matchObj.group(1)
        table_name = matchObj.group(2)
        column_name = matchObj.group(3)
        # 当前数据库绝对路径
        db_path = path.get_database_path(dv.CURRENT_DB)
        data_path = path.get_index_data_path(dv.CURRENT_DB, index_name)
        info_path = path.get_index_info_path(dv.CURRENT_DB, index_name)
        # 检查该索引是否存在
        if not os.path.exists(info_path):
            try:
                tokens = list()
                tokens.append('select')
                tokens.append(column_name)
                tokens.append('from')
                tokens.append(table_name)
                df = select.parse(tokens, True)
                df = df.sort_values(column_name)
                data_list = path.dataFrame_to_list(df)
                data = []
                for item in data_list:
                    for x in item:
                        data.append(x)
                bptree.BPlusTree(data_path, data)
                # 写入创建索引定义
                rwfile.write_to_txt(info_path, sql)
                # 将索引名写入indexes_name.txt
                rwfile.write_to_txt(db_path + r'\indexes_name.txt', index_name)
                print('CREATE INDEX ' + index_name + ' SUCCESSFUL')
            except Exception as e:
                print(e)
        else:
            print('INDEX ' + index_name + ' HAS EXIST')
    else:
        print('sql 语句格式错误')
'''

if __name__ == '__main__':
    '''
    sql_example = 'CREATE TABLE tbl (id INT PRIMARY KEY,title VARCHAR(100) NOT NULL,author VARCHAR(40) NOT NULL,submission_date DATE );'
    sql_example = sql_example.lower()
    matchOb = re.search(r'^create table (.*) \(.*\);$', sql_example)
    parse_table(sql_example)'''
    sql_example = 'CREATE INDEX student_sno ON student(sno);'
    sql_example = sql_example.lower()
    # parse_index(sql_example)
