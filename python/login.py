import pyodbc 
import os

# server = "your_server"
server = os.environ['SQL_SERVER'] # 输入要连接的服务器名称
database = 'LibraryDB'

def login(username:str,password:str):
    # Establishing a connection to the SQL Server
    cnxn = pyodbc.connect('DRIVER={SQL Server};\
                      SERVER='+server+';\
                      DATABASE='+database+';\
                      UID='+username+';\
                      PWD='+ password)

    return cnxn

def test_admin_login():
    cnxn = pyodbc.connect('DRIVER={SQL Server};\
                      SERVER='+server+';\
                      DATABASE='+database+';\
                      Trusted_Connection=yes')
    return cnxn
