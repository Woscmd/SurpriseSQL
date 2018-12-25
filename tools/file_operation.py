#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def isWhere(df, where):
    # 将字符串类型的数字转化为int
    length = len(where)
    for i in range(0, length):
        if isinstance(where[i], str) and where[i].isdigit():
            where[i] = int(where[i])

    # 满足where条件判别式
    if where[1] == '=':
        is_where = df[where[0]] == where[2]
    elif where[1] == '<':
        is_where = df[where[0]] < where[2]
    elif where[1] == '>':
        is_where = df[where[0]] > where[2]
    else:
        print('暂不支持此运算符')
        return None
    i = 3
    while i < length:
        if where[i] == 'and':
            i = i + 1
            if where[i + 1] == '=':
                is_where = is_where & (df[where[i]] == where[i + 2])
            elif where[i + 1] == '<':
                is_where = is_where & (df[where[i]] < where[i + 2])
            elif where[i + 1] == '>':
                is_where = is_where & (df[where[i]] > where[i + 2])
            else:
                print('暂不支持此运算符')
                return None
        elif where[i] == 'or':
            i = i + 1
            if where[i + 1] == '=':
                is_where = is_where | (df[where[i]] == where[i + 2])
            elif where[i + 1] == '<':
                is_where = is_where | (df[where[i]] == where[i + 2])
            elif where[i + 1] == '>':
                is_where = is_where | (df[where[i]] == where[i + 2])
            else:
                print('暂不支持此运算符')
                return None
        else:
            print('暂不支持此语法')
            return None
        i = i + 3
    return is_where

# 要删除的标签及其值
def delete(path, where):
    df = pd.read_csv(path, index_col=0)
    # 删除整个表
    if where is None:
        df = df.iloc[0:1]
        result_df = df.drop(df.index[0])
    else:
        # 将字符串类型的数字转化为int
        length = len(where)
        for i in range(0, length):
            if where[i].isdigit():
                where[i] = int(where[i])
        if where[1] == '=':
            result_df = df.loc[df[where[0]] != where[2]]
        elif where[1] == '<':
            result_df = df.loc[df[where[0]] >= where[2]]
        elif where[1] == '>':
            result_df = df.loc[df[where[0]] <= where[2]]
        else:
            print('暂不支持此运算符')
            return False
        i = 3
        while i < length:
            if where[i] == 'and':
                i = i + 1
                if where[i + 1] == '=':
                    and_df = df.loc[ df[where[i]] != where[i + 2] ]
                elif where[i + 1] == '<':
                    and_df = df.loc[ df[where[i]] >= where[i + 2] ]
                elif where[i + 1] == '>':
                    and_df = df.loc[ df[where[i]] <= where[i + 2] ]
                else:
                    print('暂不支持此运算符')
                    return False
                result_df = pd.concat([result_df, and_df], ignore_index=True)
                result_df = result_df.drop_duplicates(keep='first')
            elif where[i] == 'or':
                i = i + 1
                if where[i + 1] == '=':
                    result_df = result_df.loc[df[where[i]] != where[i + 2]]
                elif where[i + 1] == '<':
                    result_df = result_df.loc[df[where[i]] >= where[i + 2]]
                elif where[i + 1] == '>':
                    result_df = result_df.loc[df[where[i]] <= where[i + 2]]
                else:
                    print('暂不支持此运算符')
                    return False
            else:
                print('暂不支持此语法')
                return False
            i = i + 3
    result_df = result_df.reset_index(drop = True)
    print(result_df)
    result_df.to_csv(path, encoding='utf-8')
    return True

def update(path, set_value, where):
    df = pd.read_csv(path, index_col=0)
    # 将字符串类型的数字转化为int
    if set_value[2].isdigit():
       set_value[2] = int(set_value[2])

    # 更新某列所有值
    if where is None:
        df[set_value[0]] = set_value[2]
        df.to_csv(path, encoding='utf-8')
        return True
    else:
        is_where = isWhere(df, where)
        if is_where is None:
            return False
        df.loc[is_where, set_value[0]] = set_value[2]
        df = df.reset_index(drop=True)
        print(df)
        df.to_csv(path, encoding='utf-8')
        return True

def insert(path, columns, data):
    df = pd.read_csv(path, index_col=0)
    new_df = pd.DataFrame(data, columns=columns).fillna('null')
    df = df.append(new_df, ignore_index=True)
    df.to_csv(path, encoding='utf-8')
    print(df)
    return True


def select(path, columns, where, group):
    df = pd.read_csv(path, index_col=0)
    if where and isinstance(where[2], str):
        # 将字符串类型的数字转化为int
        if where[2].isdigit():
            where[2] = int(where[2])

    if where:
        is_where = isWhere(df, where)
        if is_where is None:
            return False
        df = df.loc[is_where]
        if columns[0] == '*':
            return df
        else:
            return df[columns]
    if group:
        df = df[columns].groupby(group)
        return df

    if columns[0] == '*':
        return df
    else:
        return df[columns]


if __name__ == '__main__':
    path_e = r'C:\SurpriseSQL\data\test\tables\student_data.csv'
    col = ['sno', 'sname', 'ssex', 'sbirthday', 'sclass']
    value = ['110', 'zhangsan', '男', 'null', '225']
    values = []
    values.append(value)
    insert(path_e, col, values)