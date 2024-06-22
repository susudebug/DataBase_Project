from login import admin_login
from returnValue import *
import pyodbc
from datetime import datetime

def update_fines():
    try:
        cnxn = admin_login()
        cursor = cnxn.cursor()
        
        # 获取当前日期
        current_date = datetime.now().date()
        
        # 查询未还图书
        query_unreturned = """
        SELECT borrow_id, due_date
        FROM borrow_info
        WHERE return_date IS NULL
        """
        
        # 查询已还图书
        query_returned = """
        SELECT borrow_id, due_date, return_date
        FROM borrow_info
        WHERE return_date IS NOT NULL
        """

        # 更新罚款金额
        update_query = """
        UPDATE borrow_info
        SET fine = ?
        WHERE borrow_id = ?
        """

        # 处理未还图书
        cursor.execute(query_unreturned)
        unreturned_books = cursor.fetchall()
        for book in unreturned_books:
            borrow_id, due_date_str = book
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            days_overdue = (current_date - due_date).days
            fine = max(0, days_overdue) * 0.5  # 每天1元
            cursor.execute(update_query, (fine, borrow_id))

        # 处理已还图书
        cursor.execute(query_returned)
        returned_books = cursor.fetchall()
        for book in returned_books:
            borrow_id, due_date_str, return_date_str = book
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
            days_overdue = (return_date - due_date).days
            fine = max(0, days_overdue) * 0.5  # 每天1元
            cursor.execute(update_query, (fine, borrow_id))

        cnxn.commit()

        # 查询所有借阅记录
        query_all = """
        SELECT borrow_id, library_card_number, ISBN, borrow_date, due_date, return_date, fine
        FROM borrow_info
        """
        cursor.execute(query_all)
        all_borrow_records = cursor.fetchall()
        # 打印所有借阅记录
        borrow_records = []
        for record in all_borrow_records:
            borrow_records.append({
                "borrow_id": record[0],
                "library_card_number": record[1],
                "ISBN": record[2],
                "borrow_date": record[3],
                "due_date": record[4],
                "return_date": record[5],
                "fine": record[6]
            })
        print(borrow_records)
        cursor.close()
        cnxn.close()


        return success('更新罚款成功')
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '更新罚款失败: ' + str(e))
    except Exception as e:
        return error(401, "错误: " + str(e))

# Example usage
result = update_fines()
print(result)
