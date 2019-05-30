# **SurpriseSQL**


## 简介

​     **SurpriseSQL**是使用Python3编写的一款数据库管理系统(DBMS)。



## 环境配置
- Python3.6.4

- 依赖的Python第三方库：
  numpy == 1.15.3
  
  pandas  == 0.23.4
  
  getpass

  

## 界面预览

### 登陆界面

![登陆界面](https://github.com/Woscmd/SurpriseSQL/blob/master/image/login.jpg)

  ### 主界面

![welcome](https://github.com/Woscmd/SurpriseSQL/blob/master/image/main.jpg)

![cmd](https://github.com/Woscmd/SurpriseSQL/blob/master/image/3.jpg)



## 文件说明

1. data/目录下存储数据库数据，并以csv文件存储。每一张表、视图、索引及其信息都是用一个文件存储（读写过程中小概率出现文件编码问题，建议对csv文件的编码统一编码）。
2. sql/目录下包含了SQL解析文件。
3. tool/目录下提供了最基础的I/O操作、索引的建立。
4. user/目录下存储用户数据及权限。管理员及普通用户存储在user/user_pwd.txt，若要添加用户，可在user_pwd.txt文件下直接添加。
5. main.py是主函数。



## 功能说明

1. 管理员具有授权与收回的权限。

2. 输入“help database”命令，输出所有数据表、视图和索引的信息，同时显示其对象类型；输入“help table 表名”命令，输出数据表中所有属性的详细信息；输入“help view 视图名”命令，输出视图的定义语句；输入“help index 索引名”命令，输出索引的详细信息。

3. 解析CREATE、SELECT、INSERT、DELETE、UPDATE等SQL语句的内容；能够检查SQL语句中的语法错误和语义错误。

4. 执行CREATE语句，创建数据表、视图、索引三种数据库对象；创建数据表时包含主码、外码、唯一性约束、非空约束等完整性约束的定义。

5. 执行SELECT语句，输出结果；在SELECT语句中支持GROUP BY子句，支持5种聚集函数；{单表查询、连接查询、嵌套查询、集合查询；where语句支持and、or谓词、支持分组功能}。

6. 执行INSERT、DELETE和UPDATE语句，更新数据表的内容；更新过程中需要检查更新后的数据表是否会违反参照完整性约束。支持单个元组的插入和元组集合的插入（带子查询）

7. 支持创建B+树索引。

8. 用户密码MD5加密。

9. SQL语句可参考sql.txt 。

   

## notice

1. 初始提供的用户

   | 用户名 | 密码  | 权限                                         |
   | ------ | ----- | -------------------------------------------- |
   | root   | root  | 管理员权限                                   |
   | hello  | hello | 普通用户权限（具体可参考文件permission.csv） |

   

2. pycharm2018.2暂不支持getpass库（提示用户输入密码而不回显）。

3. 双击main.py文件即可运行。

