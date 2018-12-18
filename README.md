# DBMS written in Python3
**SurpriseSQL使用Python3编写**

### 环境配置
- Python3.6.4
- PyCharm2018.2
- 依赖的Python库：csv、re、numpy、pandas、getpass(pycharm2018.2不支持此库)

### 说明
1. 管理员具有授权与收回的权限
2. 此数据库支持的命令请看help.txt
3. 管理员及普通用户可在user/user_pwd.txt查看，若要添加用户，可在user_pwd.txt文件下直接添加
4. 数据均存储在/data目录下，每一张表、视图、索引及其信息都是用一个文件存储（读写过程中小概率出现文件编码问题，建议对csv文件的编码统一编码）

