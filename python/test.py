from login import *

if __name__=="__main__":
    state = register("abc","123456")
    if state["success"]==True:
        account=state['data']
        print("创建账号成功"+str(account))
    else:
        print(state["message"])
        exit(0)
    
    state = login(account,"123456")
    if state["success"]==True:
        account=state['data']
        print("登录账号成功"+str(account))
    else:
        print(state["message"])
        exit(0)    

"""from login import test_admin_login

cnxn = test_admin_login()
# 查询
cursor = cnxn.cursor()
cursor.execute('select * from book_info')
rows = cursor.fetchall()
for row in rows:
    print(row)

cnxn.autocommit = True
# 新增
params=('9780134685000','Effective Java','Addison-Wesley','Joshua Bloch',8,2,1)
cursor.execute('insert into book_info values(?,?,?,?,?,?,?)',params)

cursor.close()
print("新增后再查找")

cursor = cnxn.cursor()
cursor.execute('select * from book_info where ISBN=9780134685000')
row = cursor.fetchone()
if row:
    print(row)
cursor.execute("delete from book_info where ISBN='9780134685000'")
print("新建用户L2并绑定到U2")
cursor.execute("sp_addlogin 'L2','123456'")
cursor.execute("sp_adduser 'L2','U2'")
cursor.close()
cnxn.close()"""