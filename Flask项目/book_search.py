from login import admin_login
from returnValue import success, error
import pyodbc

def search_books(search_term):
    try:
        cnxn=admin_login()
        cursor=cnxn.cursor()
        cnxn.autocommit=False
        
        query = """
        SELECT * FROM book_info
        WHERE ISBN like ? OR book_title LIKE ? OR author LIKE ? OR publisher LIKE ?
        """
        search_term = f"%{search_term}%"
        cursor.execute(query, (search_term, search_term, search_term, search_term))
        
        results = cursor.fetchall()
        books = []
        for row in results:
            books.append({
                "ISBN": row.ISBN,
                "book_title": row.book_title,
                "publisher": row.publisher,
                "author": row.author,
                "total_quantity": row.total_quantity,
                "available_quantity": row.available_quantity,
                "is_borrowable": row.is_borrowable
            })
        
        cursor.close()
        cnxn.close()
        
        return success(books)
    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '查询失败: ' + str(e))
    except Exception as e:
        return error(401, "错误: " + str(e))

# Example usage
if __name__ == "__main__":
    search_term = "Python"
    result = search_books(search_term)
    print(result)
