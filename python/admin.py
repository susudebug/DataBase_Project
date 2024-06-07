from login import test_admin_login
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
        cnxn = test_admin_login()
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
        cnxn = test_admin_login()
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

        if update_fields:
            update_query = f"UPDATE reader_info SET {', '.join(update_fields)} WHERE library_card_number = ?"
            update_values.append(library_card_number)
            cursor.execute(update_query, update_values)
            cnxn.commit()
            print("读者信息更新成功")
        else:
            print("没有提供任何更新的字段")
        cursor.close()
        cnxn.close()
        return success({
            "library_card_number":library_card_number,
            "name":name,
            "gender":gender,
            "title":title,
            "available_quantity":available_quantity,
            "borrowed_quantity":borrowed_quantity, 
            "department":department, 
            "contact_number":contact_number
        })
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301,'修改读者信息失败:' + str(e))
    except Exception as e:
        return error(401,"错误"+str(e))  

# 删除读者信息的函数
def delete_reader(library_card_number):
    try:
        cnxn = test_admin_login()
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
        cnxn = test_admin_login()
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
        cnxn = test_admin_login()
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
        cnxn = test_admin_login() 
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

# 函数：查询所有读者的欠款状况
def get_reader_fines():
    try:
        cnxn = test_admin_login() 
        cursor = cnxn.cursor()
        # 查询所有读者的欠款总额的SQL语句
        select_query = """
            SELECT r.library_card_number, r.name, SUM(bi.fine) AS total_fine
            FROM reader_info r
            LEFT JOIN borrow_info bi ON r.library_card_number = bi.library_card_number
            WHERE bi.return_date IS NULL AND bi.due_date < GETDATE()
            GROUP BY r.library_card_number, r.name
        """

        cursor.execute(select_query)
        rows = cursor.fetchall()
        reader_fines_info = []
        for row in rows:
            library_card_number, name, total_fine = row
            reader_info = {
                "library_card_number": library_card_number,
                "name": name,
                "total_fine": float(total_fine) if total_fine is not None else 0.0
            }
            reader_fines_info.append(reader_info)

        cursor.close()
        cnxn.close()
        return success({"readers_fines": reader_fines_info})
    
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '查询读者欠款状况失败:' + str(e))
    except Exception as e:
        return error(401, "错误" + str(e))







