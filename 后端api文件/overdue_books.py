from login import admin_login
from returnValue import success, error
import pyodbc
from datetime import datetime

def get_overdue_books():
    try:
        cnxn=admin_login()
        cursor=cnxn.cursor()
        cnxn.autocommit=False
        
        # 查询未归还图书信息
        overdue_books_query = """
        SELECT bi.borrow_id, bi.library_card_number, bi.ISBN, bi.borrow_date, bi.due_date, DATEDIFF(day, bi.due_date, GETDATE()) AS overdue_days, bi.fine
        FROM borrow_info bi
        WHERE bi.return_date IS NULL AND bi.due_date < GETDATE()
        """
        cursor.execute(overdue_books_query)
        overdue_books = cursor.fetchall()
        
        overdue_books_data = []
        for book in overdue_books:
            overdue_books_data.append({
                "borrow_id": book.borrow_id,
                "library_card_number": book.library_card_number,
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
    result = get_overdue_books()
    print(result)
