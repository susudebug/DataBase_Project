from returnValue import *
from login import admin_login
import pyodbc
import datetime

borrow_days=90

def borrow_book(library_card_number:int,isbn:str,due_date=None,begin_date=None):
    try:
        cnxn=admin_login()
        cursor1=cnxn.cursor()
        cnxn.autocommit=False
        
        # 查询isbn和library_card_number是否合法
        cursor1.execute("select is_borrowable,available_quantity from book_info where isbn='"+isbn+"'")
        book = cursor1.fetchone()
        if not book:
            cursor1.close()
            cnxn.close()
            return error(1,"isbn不存在")
        if book[0] == 0:
            cursor1.close()
            cnxn.close()
            return error(6,"书籍不可借！")
        availiable = book[1]
        if availiable == 1:
            is_borrowable=0
        else:
            is_borrowable=1         
        cursor1.execute("select * from login_table where Account="+str(library_card_number))
        if not cursor1.fetchone():
            cursor1.close()
            cnxn.close()
            return error(2,"library_card_number不存在")
        
        # 查询借书信息，观察是否有未还清欠款
        cursor1.execute("select due_date,fine,ISBN from borrow_info where library_card_number=" + str(library_card_number) + " and return_date is null") 
        rows = cursor1.fetchall()
        now = datetime.datetime.now()
        for row in rows:
            if row[1] != 0 or row[0]<now.strftime("%Y-%m-%d"):
                cursor1.close()
                cnxn.close()
                return error(4,"有未交罚金/未在时间内归还，禁止借书")
            if row[2] == isbn:
                cursor1.close()
                cnxn.close()
                return error(5,"已经借过这本书！")                

        # 查询借书数量是否超标
        cursor1.execute("select available_quantity,borrowed_quantity from reader_info where library_card_number=" + str(library_card_number))
        row = cursor1.fetchone()
        if row[0]<=row[1]:
            cursor1.close()
            cnxn.close()
            return error(3, "借书超过上限，禁止借书")
        
        
        # 借书：插入借书信息+borrow信息更新
        cursor1.execute("update reader_info set borrowed_quantity=borrowed_quantity+1 where library_card_number=" + str(library_card_number))
        if begin_date is None:
            begin_date=now.strftime("%Y-%m-%d")
        if due_date is None:
            due_date = (now + datetime.timedelta(days=borrow_days)).strftime("%Y-%m-%d")
        cursor1.execute("INSERT INTO borrow_info (library_card_number, ISBN, borrow_date, due_date, fine)VALUES(?,?,?,?,?) ", \
                        library_card_number,str(isbn),begin_date,due_date,0)
        cursor1.execute("update book_info set available_quantity=available_quantity-1 where ISBN=?",isbn)
        cursor1.execute("update book_info set is_borrowable=? where ISBN=?",is_borrowable,isbn)

        cnxn.autocommit=True
        cursor1.commit()
        cursor1.close()
        cnxn.close()
        return success({
            "library_card_number":library_card_number,
            "isbn":isbn,
            "begin_date":begin_date,
            "due_date":due_date
        })
    except pyodbc.DatabaseError as e:
        cursor1.rollback()
        cursor1.close()
        cnxn.close()
        return error(301,'借书失败:' + str(e))
    except Exception as e:
        return error(401,"错误"+str(e))    
    
def return_book(library_card_number:int,isbn:str):
    try:
        cnxn=admin_login()
        cursor1=cnxn.cursor()
        cnxn.autocommit=False
        
        # 查询isbn和library_card_number是否合法
        cursor1.execute("select * from borrow_info where ISBN='"+isbn+"' and library_card_number="+str(library_card_number))
        if not cursor1.fetchone():
            cursor1.close()
            cnxn.close()
            return error(1,"不存在借书记录!")
        
        now = datetime.datetime.now()
        nowtime = now.strftime("%Y-%m-%d")
            
        # 还书
        cursor1.execute("update reader_info set borrowed_quantity=borrowed_quantity+1 where library_card_number=" + str(library_card_number))
        cursor1.execute("update borrow_info set return_date=? where library_card_number=? and ISBN=?",nowtime, library_card_number,str(isbn))
        cursor1.execute("update book_info set available_quantity=available_quantity+1 where ISBN=? ",isbn)
        cursor1.execute("update book_info set is_borrowable=1 where ISBN=? ",isbn)
        cursor1.execute("update borrow_info set fine=0 where ISBN=? ",isbn)

        # 查找读者信息
        end_time = now + datetime.timedelta(days=7)
        cursor1.execute("select ISBN,borrow_date,due_date,fine from borrow_info where library_card_number=? and due_date<? and return_date is NULL",str(library_card_number),end_time.strftime("%Y-%m-%d")) 
        books = cursor1.fetchall()
        ret = []
        for book in books:
            cursor1.execute("select book_title from book_info where ISBN=?",book.ISBN)
            book_title = cursor1.fetchall()[0]
            ret.append({
                "ISBN":book.ISBN,
                "book_title":book_title,
                "borrow_date":book.borrow_date,
                "due_date":book.due_date,
                "fine":book.fine
            })
        cnxn.autocommit=True
        cursor1.commit()
        cursor1.close()
        cnxn.close()
        return success(ret)
    except pyodbc.DatabaseError as e:
        cursor1.rollback()
        cursor1.close()
        cnxn.close()
        return error(301,'还书失败:' + str(e))
    except Exception as e:
        return error(401,"错误"+str(e))        
    