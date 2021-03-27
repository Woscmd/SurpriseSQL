#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

# [row, row, ....]
def read_from_txt(txt_path):
    data = []
    with open(txt_path, 'r') as f:
        for line in f.readlines():
            data.append(line.replace('\n', ''))
    return data

# [[row],[row]]
def read_from_csv(csv_path):
    data = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        file = csv.reader(f)
        for item in file:
            data.append(item)
    return data

# 以追加的方式写入
def write_to_txt(txt_path, data):
    try:
        with open(txt_path, 'a+') as f:
            f.write(data + '\n')
    except Exception as e:
        print(e)
        print('Data write failed !!! ')

# 日志文件文件的写入
def write_to_log_txt(f, log):
    log_value = log.get()
    f.write(log_value + '\n')


# data is Two-dimensional list
def write_to_csv(csv_path, data):
    try:
        with open(csv_path, 'a+', newline='', encoding='utf-8') as f:
            file = csv.writer(f)
            for item in data:
                file.writerow(item)
    except Exception as e:
        print(e)
        print('Data write failed !!! ')

# [row, row, ....]
def delete_from_txt(txt_path, data):
    with open(txt_path, 'r') as r:
        lines = r.readlines()
    with open(txt_path, 'w') as w:
        for line in lines:
            if line.strip('\n') not in data:
                w.write(line)

# data is Two-dimensional list
def delete_from_csv(csv_path, data):
    read_data = []
    with open(csv_path, 'r') as r:
        read_lines = csv.reader(r)
        for line in read_lines:
            read_data.append(line)
    with open(csv_path, 'w', newline='') as w:
        file = csv.writer(w)
        for line in read_data:
            if line not in data:
                file.writerow(line)


if __name__ == '__main__':
    c_path = r'C:\SurpriseSQL\permission.csv'
    t_path = r'C:\SurpriseSQL\test.txt'
    dat1 = [['user', 'database', 'type', 'name', 'have', 'grant'], ['root', '*', '*', '*', '*', '*']]
    dat2 = [['hello', 'test', 'table', 'tbl', '*', '*'],]
    dat3 = [['hi', 'test' 'table', 'tbl', 'select,update', 'select,update']]
    dat4 = ['g','1']
    # write_to_csv(path, dat2)
    delete_from_csv(c_path, dat2)
