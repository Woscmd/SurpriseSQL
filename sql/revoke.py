#!/usr/bin/env python3
# -*- coding: utf8 -*-

import re
from base.common import get_all_user
from base.path import get_permission_path
from base.common import get_user_permissions
import base.default_variable as dv
from disk.rwfile import write_to_csv
from disk.rwfile import delete_from_csv

# 当前用户是否有收回的权限
def is_revoke():
    if dv.CURRENT_USER in dv.DATABASE_ADMIN:
        return True
    return False


# 回收权限解析
def parse(sql):
    if not is_revoke():
        print("本用户不是管理员用户，没有收权权限")
        return
    matchObj = re.search(r'^revoke (.*) on (table|view|index) (.*) from (.*);$', sql)
    if matchObj:
        permissions = matchObj.group(1).split(',')
        dbobj_type = matchObj.group(2)
        dbobj_names = matchObj.group(3).split(',')
        users = matchObj.group(4).split(',')
        existed_users = get_all_user()
        result_permissions = [] # 收回权限之后的剩余权限
        delete_rows = [] # 删除的记录行
        path = get_permission_path()
        for user in users:
            if user not in existed_users:
                print('用户%s不存在' % user)
                continue
            if user == dv.CURRENT_USER:
                print('无法收回本用户权限')
                continue
            user_permission = get_user_permissions(user, dv.CURRENT_DB)
            if not user_permission:
                print('该用户在当前数据库没有权限')
                continue
            for dbobj_name in dbobj_names:
                try:
                    for item in user_permission:
                        if (item[2] == dbobj_type or item[2] == '*') and (item[3] == dbobj_name or item[3] == '*'):
                            delete_rows.append(item)
                            # 计算收回权限之后的剩余权限
                            if item[4] == '*':
                                have_list = ['select', 'insert', 'update', 'delete', 'create']
                            else:
                                have_list = item[4].strip('\"').split(',')
                            result_list = list(set(have_list) - set(permissions))
                            result_string = ','.join(result_list)
                            # 收回权限之后的权限列表
                            result_permissions.append([item[0], item[1], item[2], item[3], result_string])
                            print('收回用户%s %s %s权限成功' % (item[0], item[2], item[3]))
                except:
                    print('收回用户%s %s %s权限失败' % (user, dbobj_type, dbobj_name))
        delete_from_csv(path, delete_rows)  # 删除权限记录
        write_to_csv(path, result_permissions) # 重写权限
    else:
        print('SQL 语法错误')


if __name__ == '__main__':
    sql_example = 'revoke select on table tbl from hello;'
    parse(sql_example)
