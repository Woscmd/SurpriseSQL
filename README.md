# DBMS written in Python3
**SurpriseSQL使用Python3编写**

### 环境配置
Python3.6.4
PyCharm2018.2
依赖的Python库：csv、re、numpy、pandas、getpass(pycharm2018.2不支持此库)

### 说明
1. 管理员具有授权与收回的权限
2. 管理员及普通用户可在user/user_pwd.txt查看，若要添加用户，可在user_pwd.txt文件下直接添加
3. 数据均存储在/data目录下，每一张表、视图、索引及其信息都是用一个文件存储（读写过程中小概率出现文件编码问题，建议对csv文件的编码统一编码）

### 功能
1. 输入“use database_name”切换数据库，默认数据库是main数据库
2. 输入“help database”命令，输出所有数据表、视图和索引的信息，同时显示其对象类型；输入“help table 表名”命令，输出数据表中所有属性的详细信息；输入“help view 视图名”命令，输出视图的定义语句；输入“help index 索引名”命令，输出索引的详细信息
3. 解析CREATE、SELECT、INSERT、DELETE、UPDATE等SQL语句的内容；检查SQL语句中的语法错误和语义错误
4. 支持CREATE语句，创建数据表、视图、索引三种数据库对象；创建数据表时包含主码、外码、唯一性约束、非空约束等完整性约束的定义
5. 支持SELECT语句，包含嵌套查询、集合查询、链接查询（只支持两个SELECT语句），where语句支持and、or谓词、支持分组功能，支持GROUP BY子句
6. 支持INSERT、DELETE和UPDATE语句，更新数据表的内容；更新过程中需要检查更新后的数据表是否会违反参照完整性约束。INSERT支持单个元组的插入和元组集合的插入（带子查询）
7. 支持GRANT语句，为用户授予对某数据库对象的CREATE、SELECT、INSERT、DELETE、UPDATE等权限；支持REVOKE语句，收回上述权限；

   __*SQL语句可查看sql.txt*__
