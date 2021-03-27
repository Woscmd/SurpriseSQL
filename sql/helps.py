#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base.path as base
import disk.rwfile as rwfile
import base.default_variable as dv

def parse(token):
    path = base.get_database_path(dv.CURRENT_DB)
    # 输出所有数据表、视图和索引的信息及其对象类型
    if token[1] == 'database':
        tables_name = rwfile.read_from_txt(path + r'\tables_name.txt')
        print('所有的数据表:')
        for table in tables_name:
            print(table)

        views_name = rwfile.read_from_txt(path + r'\views_name.txt')
        print('所有的视图:')
        for view in views_name:
            print(view)

        indexes_name = rwfile.read_from_txt(path + r'\indexes_name.txt')
        print('所有的索引:')
        for index in indexes_name:
            print(index)

    # 输出数据表中所有属性的详细信息
    elif token[1] == 'table':
        tables_name = rwfile.read_from_txt(path + r'\tables_name.txt')
        for table in tables_name:
            csv_path = base.get_table_info_path(dv.CURRENT_DB, table)
            content = rwfile.read_from_csv(csv_path)
            print(table + '表中所有属性的详细信息')
            for x in content:
                for y in x:
                    print('%20s' % y, end = '')
                print()

    # 输出视图的定义语句
    elif token[1] == 'view':
        views_name = rwfile.read_from_txt(path + r'\views_name.txt')
        for view in views_name:
            txt_path = base.get_view_info_path(dv.CURRENT_DB, view)
            content = rwfile.read_from_txt(txt_path)
            print(view + '定义语句:')
            for item in content:
                print(item)

    # 输出索引的详细信息
    elif token[1] == 'index':
        indexes_name = rwfile.read_from_txt(path + r'\indexes_name.txt')
        for index in indexes_name:
            txt_path = base.get_index_info_path(dv.CURRENT_DB, index)
            content = rwfile.read_from_txt(txt_path)
            print(index + '详细信息:')
            for item in content:
                print(item)

    else:
        print("语法错误!!!")


if __name__ == '__main__':
    parse(['help', 'database'])