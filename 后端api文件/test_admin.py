from admin import *
def test_admin_reader():
    # 打印所有读者信息
    print("Initial reader info:")
    result = print_all_reader_info()
    print(result)
    
    # 添加读者
    print("\nAdding a new reader:")
    result = add_reader(
        library_card_number=1,
        name="张三",
        gender="男",
        title="教授",
        contact_number="12345678901",
    )
    print(result)
    
    # 打印所有读者信息
    print("\nReader info after adding a new reader:")
    result = print_all_reader_info()
    print(result)
    
    # 更新读者信息
    print("\nUpdating reader info:")
    result = update_reader(
        library_card_number=1,
        name="李四",
        title="副教授",
        contact_number="09876543210"
    )
    print(result)
    
    # 打印所有读者信息
    print("\nReader info after updating:")
    result = print_all_reader_info()
    print(result)
    
    # 打印指定读者信息
    print("\nGetting reader info for library_card_number=1:")
    result = get_reader_info(1)
    print(result)
    
    print("\nGetting reader info for library_card_number=200 (non-existent):")
    result = get_reader_info(200)
    print(result)
    
    # 删除读者信息
    print("\nDeleting reader with library_card_number=1:")
    result = delete_reader(library_card_number=1)
    print(result)
    
    # 打印所有读者信息
    print("\nReader info after deleting the reader:")
    result = print_all_reader_info()
    print(result)



def test_admin_book_borrow():
    # result=get_overdue_books()
    # print(result['data']['overdue_books'])
    # result=result['data']['overdue_books']
    # for book in result:
    #     print(book['borrow_id'])
    result=get_reader_fines()
    print(result)
    # result=add_book(isbn='978-0-12-377778-9',book_title='云边有个小卖部',publisher='XMU信息学院')
    # print(result)

# test_admin_reader()
test_admin_book_borrow()

