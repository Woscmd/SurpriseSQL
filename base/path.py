#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base.default_variable as dv

# path
def get_database_path(database_name):
    return r'%s\%s' % (dv.DATA_PATH, database_name)

# table
def get_table_data_path(database_name, tb_name):
    return r'%s\%s\tables\%s_data.csv' % (dv.DATA_PATH, database_name, tb_name)

def get_table_info_path(database_name, tb_name):
    return r'%s\%s\tables\%s_info.csv' % (dv.DATA_PATH, database_name, tb_name)

# view
def get_view_data_path(database_name, view_name):
    return r'%s\%s\views\%s_data.csv' % (dv.DATA_PATH, database_name, view_name)

def get_view_info_path(database_name, view_name):
    return r'%s\%s\views\%s_info.txt' % (dv.DATA_PATH, database_name, view_name)

# index
def get_index_data_path(database_name, index_name):
    return r'%s\%s\indexes\%s_data.txt' % (dv.DATA_PATH, database_name, index_name)

def get_index_info_path(database_name, index_name):
    return r'%s\%s\indexes\%s_info.txt' % (dv.DATA_PATH, database_name, index_name)

def get_permission_path():
    return r'%s\user\permission.csv' % dv.PROJECT_PATH
