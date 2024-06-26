import pyodbc 
import os
from returnValue import *

server = ""
# server = os.environ[''] # 输入要连接的服务器名称
database = 'LibraryDB'

def admin_login():
    cnxn = pyodbc.connect('DRIVER={SQL Server};\
                      SERVER='+server+';\
                      DATABASE='+database+';\
                      Trusted_Connection=yes')
    return cnxn


def register(name:str,password:str,title:str,phone_number:str,department:str,gender:str,is_root=0)->dict:
    """
    输入:连接，要输入的密码信息,account为自动分配,然后要输入名字
    输出:系统生成的account
    """
    if len(name)<=0:
        return error(1,'姓名不能为空!')
    if len(password)<=0:
        return error(2,'密码不能为空!')
    if len(name)>50:
        return error(3,'姓名需要在1-50字符之间')
    if len(password)>50:
        return error(4,'密码须在1-50字符之间')
    if is_root != 0 and is_root != 1:
        return error(10,'权限设置错误')
    if len(title)>50:
        return error(20,"身份长度过长")
    if gender != '男' and gender != '女' and len(gender)!=0:
        return error(21,"性别只能为男或女")
    if len(department)>100:
        return error(22,"系别长度过长")
    if len(phone_number)>15:
        return error(23,"电话长度过长")
    try:
        cnxn = admin_login()
        cnxn.autocommit=False
        cursor1 = cnxn.cursor()
        account = len(cursor1.execute('select * from login_table').fetchall()) + 1
        cursor1.close()

        cursor1=cnxn.cursor()
        cursor1.execute("insert into login_table(Password,Role) values(?,?)",password,is_root)
        cursor1.execute("insert into reader_info(library_card_number,name) values(?,?)",account,name)
        if len(title)>0:
            cursor1.execute("update reader_info set title=? where library_card_number=?",title,account)
        if len(gender)>0:
            cursor1.execute("update reader_info set gender=? where library_card_number=?",gender,account)
        if len(department)>0:
            cursor1.execute("update reader_info set department=? where library_card_number=?",department,account)
        if len(phone_number)>0:
            cursor1.execute("update reader_info set phone_number=? where library_card_number=?",phone_number,account)
        cursor1.commit()
        cnxn.autocommit=True
        cursor1.close()
        cnxn.close()
        return success(account)
    except pyodbc.DatabaseError as e:
        cursor1.rollback()
        cursor1.close()
        cnxn.close()
        return error(301,'注册失败:' + str(e))
    except Exception as e:
        return error(401,'错误：'+str(e))
    

def login(account:int,password:str):
    """
    输入:用户名与密码
    输出:是否匹配,以及isadmin
    """
    try:
        cnxn = admin_login()
        cnxn.autocommit=False
        cursor1 = cnxn.cursor()
        cursor1.execute("select Role from login_table where Account="+str(account)+" and Password='"+password+"'")
        role = cursor1.fetchone()
        if role is None:
            cursor1.close()
            cnxn.close()
            return error(1,"用户名或密码错误")
        
        cursor1.close()
        cnxn.close()
        return success(role)
    except pyodbc.DatabaseError as e:
        cursor1.rollback()
        cursor1.close()
        cnxn.close()
        return error(301,'登录失败:' + str(e))
    except Exception as e:
        return error(401,"错误"+str(e))
    
    
