# DBMS written in Python3
**SurpriseSQL使用Python3编写**

### 环境配置
Python3.6.4
PyCharm2018.2
依赖的Python库：csv、re、numpy、pandas、getpass(pycharm2018.2不支持此库)

### 说明
1. 管理员具有授权与收回的权限
2. 此数据库支持的命令请看help.txt
3. 管理员及普通用户可在user/user_pwd.txt查看，若要添加用户，可在user_pwd.txt文件下直接添加
4. 数据均存储在/data目录下，每一张表、视图、索引及其信息都是用一个文件存储（读写过程中小概率出现文件编码问题，建议对csv文件的编码统一编码）
5.  user目录下存储权限文件和用户文件
6. sql目录主要包含了helps、create、select、insert、update、delete、permission七个子模块。每个子模块对相应的SQL语句进行语法分析和检查语法错误和语义错误，若语义符合规则，则执行相应的操作，否则，报告SQL语句错误
7. tools目录包含了base、bptree、default_variable、file_operation、rwfile五个子模块。base模块提供了基本的目录和文件路径，bptree模块实现了B+树的创建、数据插入和查询、叶子结点的文件写入，default_variable模块提供了基本的默认变量，file_operation模块实现了select、insert、update、delete语句与文件的关联，rwfile模块提供了对文件读写操作的支持。

