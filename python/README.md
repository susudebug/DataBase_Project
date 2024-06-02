# Database 图书馆

安装库

```bash
pip install -r requirements.txt
```

用pyodbc的库进行数据库与python连接，[pyodbc wiki](https://github.com/mkleehammer/pyodbc/wiki)  
注意:

(1)要将login.py中server改成自己的server  

```python
server = 'your_server' # 输入要连接的服务器名称
```

(2)要在api建立连接后要设置cnxn.autocommit=False,类似于下面代码

```python
try:
    cnxn.autocommit = False
    params = [ ('A', 1), ('B', 2) ]
    cursor.executemany("insert into t(name, id) values (?, ?)", params)
except pyodbc.DatabaseError as err:
    cnxn.rollback()
else:
    cnxn.commit()
finally:
    cnxn.autocommit = True
```

返回出错和正确统一用returnValue.py中的success和error函数，在文件前面import进去就好。
