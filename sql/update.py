#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import tools.file_operation as fop
import tools.default_variable as dv
from tools.base import check_permission
from tools.base import get_table_data_path

def parse(sql):
    if 'where' not in sql:
        matchObj = re.search(r'^update (.*) set (.*);$', sql)
        if matchObj:
            table_name = matchObj.group(1)
            if not check_permission(table_name, 'update'):
                print('本用户没有对表%s %s权限' % (table_name, 'UPDATE'))
                return
            path = get_table_data_path(dv.CURRENT_DB, table_name)
            fop.update(path, None)
        else:
            print("SQL 语法错误")
    elif 'where' in sql:
        matchObj = re.search(r'update (.*) set (.*) where (.*);$', sql)
        if matchObj:
            table_name = matchObj.group(1)
            value = matchObj.group(2)
            constraint = matchObj.group(3)
            if not check_permission(table_name, 'update'):
                print('本用户没有对表%s %s权限' % (table_name, 'UPDATE'))
                return
            path = get_table_data_path(dv.CURRENT_DB, table_name)
            where = constraint.strip().split(' ')
            set_value = value.strip().split(' ')
            if fop.update(path, set_value, where):
                print('更新成功')
            else:
                print('更新失败')
        else:
            print("SQL 语法错误")
    else:
        print("SQL 语法错误")



if __name__ == '__main__':
    sql_example = 'update student set sclass = 225 where sclass = 95031 or ssex = 男;'
    parse(sql_example)
