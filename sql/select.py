#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base.default_variable as dv
from base.path import get_table_data_path
from disk import file_operation as fop
from tools.integrity import check_permission
from base.common import dataFrame_to_list
import pandas as pd
from base.common import is_table
from base.common import get_view_definition

# 单表查询
def singleSelect(tokens):
    try:
        from_index = tokens.index('from')
    except:
        print('SQL 语法错误')
        return False
    columns = tokens[1:from_index]
    table = tokens[from_index + 1]
    where = list()
    group = None
    if 'where' in tokens:
        where_index = tokens.index('where')
        where = tokens[where_index + 1:]

    if not check_permission(table, 'select'):
        print('本用户没有对表%s %s权限' % (table, 'SELECT'))
        return False
    path = get_table_data_path(dv.CURRENT_DB, table)
    data = fop.select(path, columns, where, group)
    return data

def parseView(view_name):
    tokens = get_view_definition(view_name)
    data = singleSelect(tokens)
    print(data)

# 嵌套查询
def nestedSelect(tokens):
    try:
        first_index = tokens.index('(')
        final_index = tokens.index(')')
    except:
        print('SQL 语法错误')
        return False
    child_tokens = tokens[first_index + 1:final_index]
    if not child_tokens:
        return False
    where_values = singleSelect(child_tokens)
    # dataFrame转化成二维list
    where_values = dataFrame_to_list(where_values)
    # 二维list转化一维list
    where_values = [n for a in where_values for n in a]
    return where_values


def parse(tokens, is_return=False):
    try:
        from_index = tokens.index('from')
    except:
        print('SQL 语法错误')
        return
    group_index = -1
    columns = tokens[1:from_index]
    table = tokens[from_index + 1]
    # 判断是否为视图
    if not is_table(table):
        parseView(table)
        return
    where = list()
    group = None
    join_flag = False
    if 'group' in tokens:
        group_index = tokens.index('group')
        group = tokens[group_index + 2]
    if 'where' in tokens:
        where_index = tokens.index('where')
        if group_index == -1:
            where = tokens[where_index + 1:]
        else:
            where = tokens[where_index + 1:group_index + 1]
        if where_index - from_index > 2:
            join_flag = True
    if not check_permission(table, 'select'):
        print('本用户没有对表%s %s权限' % (table, 'SELECT'))
        return
    path = get_table_data_path(dv.CURRENT_DB, table)

    # 嵌套查询
    if 'select' in where:
        where[1] = '='
        result = nestedSelect(where)
        where = where[0:3]
        if not result:
            return
        for item in result:
            where[2] = item
            data = fop.select(path, columns, where, group)
            if not data.empty:
                print(data)
    # 集合查询
    # 并集
    elif 'union' in tokens:
        union_index = tokens.index('union')
        select1 = tokens[:union_index]
        select2 = tokens[union_index+1:]
        data1 = singleSelect(select1)
        data2 = singleSelect(select2)
        result_df = pd.concat([data1, data2]).drop_duplicates()
        result_df = result_df.reset_index(drop=True)
        print(result_df)
    # 交集
    elif 'intersect' in tokens:
        intersect_index = tokens.index('intersect')
        select1 = tokens[:intersect_index]
        select2 = tokens[intersect_index + 1:]
        data1 = singleSelect(select1)
        data2 = singleSelect(select2)
        column = data1.columns.values.tolist()
        result_df = pd.merge(data1, data2, on=column)
        result_df = result_df.reset_index(drop=True)
        print(result_df)
    # 差集
    elif 'except' in tokens:
        except_index = tokens.index('except')
        select1 = tokens[:except_index]
        select2 = tokens[except_index + 1:]
        data1 = singleSelect(select1)
        data2 = singleSelect(select2)
        column = data1.columns.values.tolist()
        data1 = data1.append(data2)
        data1 = data1.append(data2)
        data1 = data1.drop_duplicates(subset=column, keep=False)
        print(data1)
    # 连接查询
    elif join_flag:
        table1 = where[0].split('.')[0]
        table2 = where[2].split('.')[0]
        table1_path = get_table_data_path(dv.CURRENT_DB, table1)
        table2_path = get_table_data_path(dv.CURRENT_DB, table2)
        df1 = fop.select(table1_path, ['*'], [], [])
        df2 = fop.select(table2_path, ['*'], [], [])
        join_column = where[0].split('.')[1]
        result_df = pd.merge(df1, df2, on=join_column)
        if len(where) > 3:
            where = where[4:]
            is_where = fop.isWhere(result_df, where)
            result_df = result_df.loc[is_where]
        result_df = result_df[columns]
        print(result_df)
    # 单表查询
    else:
        data = fop.select(path, columns, where, group)
        if data.empty:
            print('未找到记录')
        else:
            if is_return:
                return data
            else:
                if data is None:
                    print('SQL 语法错误')
                else:
                    print(data)


if __name__ == '__main__':
    # parse(['select', 'sno', 'sname', 'ssex', 'from', 'student'])
    # parse(['select', 'sno','sname','ssex', 'from', 'student','group','by','ssex'])
    # parse(['select', 'sno', 'sname', 'from', 'student', 'where', 'sclass', '=', '225', 'or', 'ssex', '=', '男'])
    # parse(['select', 'sno', 'sname', 'from', 'student', 'where', 'sno', 'in', '(', 'select', 'sno', 'from', 'score', 'where', 'cno', '=', '3-105', ')'])
    # parse(['select', 'sno', 'from', 'score', 'where', 'cno', '=', '3-105'])
    # parse(['select', 'sno','from', 'student','intersect','select', 'sno', 'from', 'score', 'where', 'cno', '=', '3-105'])
    # parse(['select', 'sno', 'sname', 'degree','from', 'student','score', 'where', 'student.sno', '=', 'score.sno'])
    parseView('student')
