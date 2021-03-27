#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from tools.integrity import check_permission
from tools.integrity import check_constraint
from base.common import get_all_columns
from base.common import get_table_data_path
import base.default_variable as dv
import disk.file_operation as fop
import sql.select as select
from base.common import string_to_token
from base.common import dataFrame_to_list

def parse(sql):
    if 'values' in sql:
        matchObj = re.search(r'^insert into (.*)\((.*)\) values\((.*)\);$', sql)
        if matchObj:
            table_name = matchObj.group(1)
            if not check_permission(table_name, 'insert'):
                print('本用户没有对表%s %s权限' % (table_name, 'INSERT'))
                return
            columns = matchObj.group(2).split(',')
            values = matchObj.group(3).split(',')
            c_v = dict(zip(columns, values))
            data = list()
            insert_data = []
            # 定义表时的列
            define_columns = get_all_columns(table_name)
            if check_constraint(table_name, c_v):
                for column in define_columns:
                    if column in columns:
                        data.append(c_v[column])
                    else:
                        data.append('null')
                insert_data.append(data)
                path = get_table_data_path(dv.CURRENT_DB, table_name)
                if fop.insert(path, define_columns, insert_data):
                    print("插入%s表%s成功" % (table_name, columns))
                else:
                    print("插入%s表%s失败" % (table_name, columns))
            else:
                print('约束条件不满足')
        else:
            print("SQL 语法错误")
    elif 'select' in sql:
        matchObj = re.search(r'^insert into (.*)\((.*)\) (.*);$', sql)
        if matchObj:
            table_name = matchObj.group(1)
            if not check_permission(table_name, 'insert'):
                print('本用户没有对表%s %s权限' % (table_name, 'INSERT'))
                return
            columns = matchObj.group(2).split(',')
            child_select = matchObj.group(3)
            child_select = string_to_token(child_select)
            # 查询的结果dataFrame
            data = select.parse(child_select, True)
            # 定义表时的列
            define_columns = get_all_columns(table_name)
            data_list = dataFrame_to_list(data)
            for item in data_list:
                c_v = dict(zip(columns, item))
                if not check_constraint(table_name, c_v):
                    print('约束条件不满足')
                    return
            path = get_table_data_path(dv.CURRENT_DB, table_name)
            if fop.insert(path, define_columns, data):
                print("插入%s表%s成功" % (table_name, columns))
            else:
                print("插入%s表%s失败" % (table_name, columns))
        else:
            print("SQL 语法错误")
            return
    else:
        print("SQL 语法错误")
        return


if __name__ == '__main__':
    sql_example = "insert into student(sno,sname,ssex,sclass) values(101,张三,男,225);"
    sql_example = "insert into student_s(sno,sname,ssex,sclass) select sno,sname,ssex,sclass from student;"
    parse(sql_example)
