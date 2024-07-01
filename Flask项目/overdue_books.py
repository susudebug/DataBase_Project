from login import admin_login, logged_in_account
from returnValue import success, error
import pyodbc
from datetime import datetime

def get_overdue_books4U(act):
    try:
        cnxn=admin_login()
        cursor=cnxn.cursor()
        cnxn.autocommit=False

        # 查询未归还图书信息
        overdue_books_query = """
        SELECT bi.borrow_id, bi.ISBN, bi.library_card_number, bi.borrow_date, bi.due_date, DATEDIFF(day, bi.due_date, GETDATE()) AS overdue_days, bi.fine
        FROM borrow_info bi
        WHERE bi.return_date IS NULL AND bi.due_date < GETDATE() and bi.library_card_number = ?
        """

        print()
        cursor.execute(overdue_books_query, act)
        overdue_books = cursor.fetchall()
        
        overdue_books_data = []
        for book in overdue_books:
            overdue_books_data.append({
                "borrow_id": book.borrow_id,
                # "library_card_number": book.library_card_number,
                "ISBN": book.ISBN,
                "borrow_date": book.borrow_date,
                "due_date": book.due_date,
                "overdue_days": book.overdue_days,
                "fine": book.fine
            })
        
        cursor.close()
        cnxn.close()
        
        return success(overdue_books_data)
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '查询失败: ' + str(e))
    except Exception as e:
        return error(401, "错误: " + str(e))

# Example usage
if __name__ == "__main__":
    result = get_overdue_books4U()
    print(result)
