from login import admin_login
from returnValue import *
import pyodbc
def print_fines_record(library_card_number):
    try:
        cnxn = admin_login()
        cursor = cnxn.cursor()

        # 查询特定读者的借阅记录，且罚款不为0
        select_query = """
SELECT b.library_card_number, r.name, b.ISBN, b.borrow_date, b.due_date, b.return_date, b.fine
FROM borrow_info b
INNER JOIN reader_info r ON b.library_card_number = r.library_card_number
WHERE b.library_card_number = ? AND b.fine > 0

            """

        cursor.execute(select_query, library_card_number)
        rows = cursor.fetchall()
        fines_info = []
        for row in rows:
            library_card_number, name, ISBN, borrow_date, due_date,return_date, fine= row
            borrow_info = {
                "library_card_number": library_card_number,
                "name": name,
                "ISBN":ISBN,
                "borrow_date":borrow_date,
                "due_date":due_date,
                "return_date":return_date,
                "fine": float(fine) if fine is not None else 0.0,
            }
            fines_info.append(borrow_info)
        cursor.close()
        cnxn.close()
        return success({"fines_info": fines_info})

    except pyodbc.DatabaseError as e:
        cursor.rollback()
        cursor.close()
        cnxn.close()
        return error(301, '查询罚款信息失败: ' + str(e))
    except Exception as e:
        return error(401, "错误: " + str(e))
