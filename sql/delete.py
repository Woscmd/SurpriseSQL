#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import tools.default_variable as dv
import tools.file_operation as fop
from tools.base import check_permission
from tools.base import get_table_data_path

def parse(sql):
    if 'where' not in sql:
        matchObj = re.search(r'^delete from (.*);$', sql)
        if matchObj:
            table_name = matchObj.group(1)
            if check_permission(table_name, 'delete'):
                print('本用户没有对表%s %s权限' % (table_name, 'DELETE'))
                return
            path = get_table_data_path(dv.CURRENT_DB, table_name)
            fop.delete(path, None)
        else:
            print("SQL 语法错误")
    elif 'where' in sql:
        matchObj = re.search(r'delete from (.*) where (.*);$', sql)
        if matchObj:
            table_name = matchObj.group(1)
            constraint = matchObj.group(2)
            if not check_permission(table_name, 'delete'):
                print('本用户没有对表%s %s权限' % (table_name, 'DELETE'))
                return
            path = get_table_data_path(dv.CURRENT_DB, table_name)
            label = constraint.strip().split(' ')
            if fop.delete(path, label):
                print('删除成功')
            else:
                print('删除失败')
        else:
            print("SQL 语法错误")
    else:
        print("SQL 语法错误")



if __name__ == '__main__':
    sql_example = 'delete from student where sclass = 95031 or sno = 101;'
    parse(sql_example)
