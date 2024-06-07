from admin import *
def test_admin_reader():
    # 打印所有读者信息
    print("Initial reader info:")
    result = print_all_reader_info()
    if result['success']==False:
        print(result)
    else:
        for reader in result["data"]["readers"]:
            print(reader)
    
    # 添加读者
    print("\nAdding a new reader:")
    result = add_reader(
        library_card_number=1,
        name="张三",
        gender="男",
        title="教授",
        contact_number="12345678901",
    )
    if result['success']==False:
        print(result)
    else:
        print(result['data'])
    
    # 打印所有读者信息
    print("\nReader info after adding a new reader:")
    result = print_all_reader_info()
    if result['success']==False:
        print(result)
    else:
        for reader in result["data"]["readers"]:
            print(reader)
    
    # 更新读者信息
    print("\nUpdating reader info:")
    result = update_reader(
        library_card_number=1,
        name="李四",
        title="副教授",
        contact_number="09876543210"
    )
    if result['success']==False:
        print(result)
    else:
        print(result['data'])
    
    # 打印所有读者信息
    print("\nReader info after updating:")
    result = print_all_reader_info()
    if result['success']==False:
        print(result)
    else:
        for reader in result["data"]["readers"]:
            print(reader)
    
    # 打印指定读者信息
    print("\nGetting reader info for library_card_number=1:")
    result = get_reader_info(1)
    if result['success']==False:
        print(result)
    else:
        print(result['data'])
    
    print("\nGetting reader info for library_card_number=200 (non-existent):")
    result = get_reader_info(200)
    if result['success']==False:
        print(result)
    else:
        print(result['data'])
    
    # 删除读者信息
    print("\nDeleting reader with library_card_number=1:")
    result = delete_reader(library_card_number=1)
    if result['success']==False:
        print(result)
    else:
        print(result)
    
    # 打印所有读者信息
    print("\nReader info after deleting the reader:")
    result = print_all_reader_info()
    if result['success']==False:
        print(result)
    else:
        for reader in result["data"]["readers"]:
            print(reader)



def test_admin_book_borrow():
    result=get_overdue_books()
    if result['success']==False:
        print(result)
    else:
        for reader in result["data"]["overdue_books"]:
            print(reader)
    result=get_reader_fines()
    if result['success']==False:
        print(result)
    else:
        for reader in result["data"]["readers_fines"]:
            print(reader)

#test_admin_reader()
test_admin_book_borrow()
