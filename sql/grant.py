#!/usr/bin/env python3
# -*- coding: utf8 -*-

import re
from base.common import get_all_user
from base.path import get_permission_path
from base.common import get_user_permissions
import base.default_variable as dv
from disk.rwfile import write_to_csv
from disk.rwfile import delete_from_csv

# 当前用户是否有授予的权限
def is_grant():
    if dv.CURRENT_USER in dv.DATABASE_ADMIN:
        return True
    return False

# 授权解析
def parse(sql):
    if not is_grant():
        print("本用户不是管理员用户，没有授权权限")
        return
    matchObj = re.search(r'^grant (.*) on (table|view|index) (.*) to (.*);$', sql)
    if matchObj:
        permissions = matchObj.group(1)
        dbobj_type = matchObj.group(2)
        dbobj_names = matchObj.group(3).split(',')
        users = matchObj.group(4).split(',')
        existed_users = get_all_user()
        path = get_permission_path()
        result_permissions = []
        delete_rows = []
        for user in users:
            if user not in existed_users:
                print('用户%s不存在' % user)
                continue
            if user == dv.CURRENT_USER:
                print('无法授予本用户权限')
                continue
            user_permission = get_user_permissions(user, dv.CURRENT_DB)
            for dbobj_name in dbobj_names:
                try:
                    # 未存在user和CURRENT_DB的记录时
                    if not user_permission:
                        result_permissions.append([user, dv.CURRENT_DB, dbobj_type, dbobj_name, permissions])
                    else:
                        for item in user_permission:
                            if (item[2] == dbobj_type or item[2] == '*') and (item[3] == dbobj_name or item[3] == '*'):
                                delete_rows.append(item)
                                delete_from_csv(path, delete_rows)  # 删除权限记录
                                # 计算授权权限之后的权限
                                if item[4] == '*':
                                    have_list = ['select', 'insert', 'update', 'delete', 'create']
                                else:
                                    have_list = item[4].strip('\"').split(',')
                                permissions = permissions.split(',')
                                result_list = list(set(have_list) | set(permissions))
                                result_string = ','.join(result_list)
                                # 授予权限之后的权限列表
                                result_permissions.append([item[0], item[1], item[2], item[3], result_string])
                            else:
                                result_permissions.append([user, dv.CURRENT_DB, dbobj_type, dbobj_name, permissions])
                    print('授予用户%s %s %s的权限成功' % (user, dbobj_type, dbobj_name))
                except:
                    print('授予用户%s %s %s的权限失败' % (user, dbobj_type, dbobj_name))
        write_to_csv(path, result_permissions)
    else:
        print('SQL 语法错误')


if __name__ == '__main__':
    sql_example = "grant select on table tbl to hello;"
    parse(sql_example)
