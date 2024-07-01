from login import admin_login
from returnValue import success, error
import pyodbc

def get_reader_info(library_card_number):
    try:
        cnxn=admin_login()
        cursor=cnxn.cursor()
        cnxn.autocommit=False
        
        # 查询个人信息
        reader_info_query = """
        SELECT * FROM reader_info
        WHERE library_card_number = ? 
        """
        cursor.execute(reader_info_query, (library_card_number,))
        reader_info = cursor.fetchone()
        
        if not reader_info:
            return error(404, "读者信息未找到")
        
        reader_data = {
            "library_card_number": reader_info.library_card_number,
            "name": reader_info.name,
            "gender": reader_info.gender,
            "title": reader_info.title,
            "available_quantity": reader_info.available_quantity,
            "borrowed_quantity": reader_info.borrowed_quantity,
            "department": reader_info.department,
            "contact_number": reader_info.contact_number
        }
        
        # 查询当前借书信息
        borrowed_books_query = """
        SELECT b.book_id, b.title, b.author, br.borrow_date, br.due_date
        FROM borrow_info br
        JOIN book_info b ON br.ISBN = b.ISBN
        WHERE br.library_card_number = ? AND br.return_date IS NULL
        """
        cursor.execute(borrowed_books_query, (library_card_number,))
        borrowed_books = cursor.fetchall()
        
        borrowed_books_data = []
        # total_fine = 0
        for book in borrowed_books:
            borrowed_books_data.append({
                "borrow_id":book.borrow_id,
#                "library_card_number":book.library_card_number,
                "ISBN": book.book_ISBN,
                "book_title": book.book_title,
                "author": book.author,
                "borrow_date": book.borrow_date,
                "due_date": book.due_date,
                "return_date": book.return_date,
                "fine": book.fine
            }
            # total_fine += book.fine
        )
        
        cursor.close()
        cnxn.close()
        
        return success({
            "reader_info": reader_data,
            "borrowed_books": borrowed_books_data,
        })
        
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '查询失败: ' + str(e))
    except Exception as e:
        return error(401, "错误: " + str(e))

# Example usage
if __name__ == "__main__":
    library_card_number = "12345678"
    result = get_reader_info(library_card_number)
    print(result)
