# DBMS written in Python3
**SurpriseSQL使用Python3编写**

### 环境配置
- Python3.6.4
- PyCharm2018.2
- 依赖的Python库：
numpy == 1.15.3 
 pandas  == 0.23.4
pycharm2018.2不支持getpass库

### 说明
1. 管理员具有授权与收回的权限
2. 管理员及普通用户可在user/user_pwd.txt查看，若要添加用户，可在user_pwd.txt文件下直接添加
3. 数据均存储在/data目录下，每一张表、视图、索引及其信息都是用一个文件存储（读写过程中小概率出现文件编码问题，建议对csv文件的编码统一编码）
4. 输入“help database”命令，输出所有数据表、视图和索引的信息，同时显示其对象类型；输入“help table 表名”命令，输出数据表中所有属性的详细信息；输入“help view 视图名”命令，输出视图的定义语句；输入“help index 索引名”命令，输出索引的详细信息
5. 解析CREATE、SELECT、INSERT、DELETE、UPDATE等SQL语句的内容；检查SQL语句中的语法错误和语义错误
6. 执行CREATE语句，创建数据表、视图、索引三种数据库对象；创建数据表时包含主码、外码、唯一性约束、非空约束等完整性约束的定义
7. 执行SELECT语句，输出结果；在SELECT语句中支持GROUP BY子句，支持5种聚集函数；{单表查询、连接查询、嵌套查询、集合查询；where语句支持and、or谓词、支持分组功能}
8. 执行INSERT、DELETE和UPDATE语句，更新数据表的内容；更新过程中需要检查更新后的数据表是否会违反参照完整性约束。支持单个元组的插入和元组集合的插入（带子查询）
9. 支持创建B+树索引
10. SQL语句可参考sql.txt 

