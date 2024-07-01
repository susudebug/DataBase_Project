from login import admin_login
from returnValue import *
import pyodbc
from datetime import datetime

'''
管理读者的相关函数
'''
# 添加读者信息的函数 --注意library_card_number的外键约束
# 可借图书总数默认为10本，已借图书数默认为0本
def add_reader(library_card_number, name=None, gender=None, title=None, available_quantity=10, borrowed_quantity=0, department=None, contact_number=None):

    try:
        cnxn = admin_login()
        cursor = cnxn.cursor()

        insert_query = """
        INSERT INTO reader_info (library_card_number, name, gender, title, available_quantity, borrowed_quantity, department, contact_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(insert_query, (library_card_number, name, gender, title, available_quantity, borrowed_quantity, department, contact_number))
        cnxn.commit()

        cursor.close()
        cnxn.close()
        return success({
            "library_card_number": library_card_number,
            "name": name,
            "gender": gender,
            "title": title,
            "available_quantity": available_quantity,
            "borrowed_quantity": borrowed_quantity,
            "department": department,
            "contact_number": contact_number
        })
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '添加读者失败: ' + str(e))
    except Exception as e:
        return error(401, "错误: " + str(e))


# 更新读者信息的函数
# 可借图书总数默认为10本，已借图书数默认为0本
def update_reader(library_card_number, name=None, gender=None, title=None, available_quantity=10, borrowed_quantity=0, department=None, contact_number=None):
    try:
        # 假设 admin_login() 是用于数据库连接的函数
        cnxn = admin_login()
        cursor = cnxn.cursor()

        update_fields = []
        update_values = []

        if name is not None:
            update_fields.append("name = ?")
            update_values.append(name)
        if gender is not None:
            update_fields.append("gender = ?")
            update_values.append(gender)
        if title is not None:
            update_fields.append("title = ?")
            update_values.append(title)
        if available_quantity is not None:
            update_fields.append("available_quantity = ?")
            update_values.append(available_quantity)
        if borrowed_quantity is not None:
            update_fields.append("borrowed_quantity = ?")
            update_values.append(borrowed_quantity)
        if department is not None:
            update_fields.append("department = ?")
            update_values.append(department)
        if contact_number is not None:
            update_fields.append("contact_number = ?")
            update_values.append(contact_number)

        if not update_fields:
            return error(44, '没有提供任何更新信息')

        update_values.append(library_card_number)
        update_query = f"UPDATE reader_info SET {', '.join(update_fields)} WHERE library_card_number = ?"
        
        cursor.execute(update_query, update_values)
        cnxn.commit()
        

        # 检查是否有更新的行数
        if cursor.rowcount == 0:
            return error(800, f"读者信息不存在：{library_card_number}")
        else:
            print("读者信息更新成功")
        cursor.close()
        cnxn.close()

        # 返回更新后的读者信息
        return success({
            "library_card_number": library_card_number,
            "name": name,
            "gender": gender,
            "title": title,
            "available_quantity": available_quantity,
            "borrowed_quantity": borrowed_quantity,
            "department": department,
            "contact_number": contact_number
        })

    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '修改读者信息失败: ' + str(e))

    except Exception as e:
        return error(401, "错误：" + str(e))
  

# 删除读者信息的函数
def delete_reader(library_card_number):
    try:
        if library_card_number==None:
            return error(218,'没有给予要删除的读者信息')
        cnxn = admin_login()
        cursor = cnxn.cursor()
        delete_query = "DELETE FROM reader_info WHERE library_card_number = ?"
        cursor.execute(delete_query, (library_card_number,))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        return success({
            "library_card_number":library_card_number
        })
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301,'删除读者信息失败:' + str(e))
    except Exception as e:
        return error(401,"错误"+str(e))  

# 查询并打印reader_info表的函数
def print_all_reader_info():
    try:
        cnxn = admin_login()
        cursor = cnxn.cursor()
        select_query = "SELECT * FROM reader_info"
        cursor.execute(select_query)
        
        rows = cursor.fetchall()
        if not rows:
            cursor.close()
            cnxn.close()
            return error(30, "reader_info表中没有读者信息")
        

        columns = [column[0] for column in cursor.description]
        all_reader_info = [dict(zip(columns, row)) for row in rows]
        
        cursor.close()
        cnxn.close()
        return success({"readers": all_reader_info})
        
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '查询读者信息失败:' + str(e))
    except Exception as e:
        return error(401, "错误" + str(e)) 

# 通过借书证号查询读者信息的函数
def get_reader_info(library_card_number):
    try:
        cnxn = admin_login()
        cursor = cnxn.cursor()
        select_query = "SELECT * FROM reader_info WHERE library_card_number = ?"
        cursor.execute(select_query, (library_card_number,))

        row = cursor.fetchone()
        if row:

            columns = [column[0] for column in cursor.description]
            reader_info = dict(zip(columns, row))
            cursor.close()
            cnxn.close()
            return success(reader_info)
        else:
            cursor.close()
            cnxn.close()
            return error(20, "未找到该借书证号对应的读者信息")
        
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '查询读者信息失败:' + str(e))
    except Exception as e:
        return error(401, "错误" + str(e))


# 函数：查询所有到期未归还的图书信息
def get_overdue_books():
    try:
        cnxn = admin_login() 
        cursor = cnxn.cursor()

        current_date = datetime.now().date().isoformat() 
        select_query = """
            SELECT bi.borrow_id, bi.library_card_number, bi.ISBN, bi.borrow_date, bi.due_date,bi.return_date
            FROM borrow_info bi
            WHERE bi.due_date < ?
            AND bi.return_date IS NULL
        """
        cursor.execute(select_query, current_date)

        rows = cursor.fetchall()


        
        overdue_books_info = []
        for row in rows:
            borrow_id, library_card_number, ISBN, borrow_date, due_date,return_date = row
            book_info = {
                "borrow_id": borrow_id,
                "library_card_number": library_card_number,
                "ISBN": ISBN,
                "borrow_date": borrow_date,
                "due_date": due_date,
                "return_date":return_date
            }
            overdue_books_info.append(book_info)
        
        cursor.close()
        cnxn.close()
        return success({"overdue_books": overdue_books_info})
    
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '查询到期未归还的图书信息失败:' + str(e))
    except Exception as e:
        return error(401, "错误" + str(e))

# 函数：添加新书
# 其中可借总数默认为10，当前可借数量默认为10
def add_book(isbn, book_title, publisher=None, author=None, total_quantity=10, available_quantity=10, is_borrowable=1):
    try:
        # 假设 admin_login 是一个返回数据库连接对象的函数
        cnxn = admin_login()
        cursor = cnxn.cursor()

        # 查询是否已存在相同的 ISBN
        check_query = "SELECT COUNT(*) FROM book_info WHERE ISBN = ?"
        cursor.execute(check_query, (isbn,))
        if cursor.fetchone()[0] > 0:
            cursor.close()
            cnxn.close()
            return {
                "status": "error",
                "code": 1000,
                "message": "图书添加失败: ISBN 已存在"
            }

        insert_query = """
        INSERT INTO book_info (ISBN, book_title, publisher, author, total_quantity, available_quantity, is_borrowable)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(insert_query,
                       (isbn, book_title, publisher, author, total_quantity, available_quantity, is_borrowable))
        cnxn.commit()

        cursor.close()
        cnxn.close()
        return {
            "status": "success",
            "data": {
                "ISBN": isbn,
                "book_title": book_title,
                "publisher": publisher,
                "author": author,
                "total_quantity": total_quantity,
                "available_quantity": available_quantity,
                "is_borrowable": is_borrowable
            }
        }
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return {
            "status": "error",
            "code": 301,
            "message": '添加图书失败: ' + str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "code": 401,
            "message": "错误: " + str(e)
        }



# 函数：查询所有读者的欠款状况
def get_reader_fines():
    try:
        cnxn = admin_login()
        cursor = cnxn.cursor()

        # 查询所有读者的欠款总额的SQL语句
        select_query = """
            SELECT r.library_card_number, r.name, SUM(bi.fine) AS total_fine, r.contact_number
            FROM reader_info r
            LEFT JOIN borrow_info bi ON r.library_card_number = bi.library_card_number
            WHERE bi.return_date IS NULL AND bi.due_date < GETDATE()
            GROUP BY r.library_card_number, r.name, r.contact_number
        """

        cursor.execute(select_query)
        rows = cursor.fetchall()
        reader_fines_info = []
        for row in rows:
            library_card_number, name, total_fine, contact_number = row
            reader_info = {
                "library_card_number": library_card_number,
                "name": name,
                "total_fine": float(total_fine) if total_fine is not None else 0.0,
                "contact_number": contact_number
            }
            reader_fines_info.append(reader_info)

        cursor.close()
        cnxn.close()
        return success({"readers_fines": reader_fines_info})

    except pyodbc.DatabaseError as e:
        if 'cursor' in locals():
            cursor.close()
        if 'cnxn' in locals():
            cnxn.close()
        return error(301, '查询读者欠款状况失败: ' + str(e))
    except Exception as e:
        return error(401, "错误: " + str(e))







