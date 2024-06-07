# 登录表(login_table)

| 列名     | 数据类型 | 长度 | 主键 | 非空 | 备注                      |
| -------- | -------- | ---- | ---- | ---- | ------------------------- |
| Account  | int      |      | Yes  | Yes  |                           |
| password | varchar  | 10   |      | Yes  |                           |
| role     | int      |      |      | Yes  | 0-读者；1-管理员；默认为0 |

# 图书信息表(book_info)

| 列名               | 数据类型 | 长度 | 主键 | 非空 | 备注               |
| ------------------ | -------- | ---- | ---- | ---- | ------------------ |
| ISBN               | varchar  | 30   | Yes  | Yes  |                    |
| book_title         | varchar  | 100  |      | Yes  |                    |
| publisher          | varchar  | 50   |      |      |                    |
| author             | varchar  | 50   |      |      |                    |
| total_quantity     | int      |      |      |      |                    |
| Available_quantity | int      |      |      |      |                    |
| is_borrowable      | bit      |      |      |      | 1为可借，0为不可借 |

# 读者信息表(reader_info)

| 列名                | 数据类型 | 长度 | 主键 | 非空 | 备注                                     |
| ------------------- | -------- | ---- | ---- | ---- | ---------------------------------------- |
| library_card_number | int      |      | Yes  |      | 外键约束，参考登录表login_table的Account |
| name                | varchar  | 50   |      | Yes  |                                          |
| gender              | varchar  | 10   |      |      | 值为“男“、”女“二选一                     |
| title               | varchar  | 50   |      |      |                                          |
| Available_quantity  | int      |      |      |      |                                          |
| borrowed_quantity   | int      |      |      |      |                                          |
| department          | varchar  | 100  |      |      |                                          |
| contact_number      | varchar  | 15   |      |      |                                          |

# 借阅信息表(borrow_info)

| 列名                | 数据类型 | 长度 | 主键 | 非空 | 备注                                  |
| ------------------- | -------- | ---- | ---- | ---- | ------------------------------------- |
| borrow_id           | int      |      | Yes  |      |                                       |
| library_card_number | int      |      |      |      | 外键约束，参考读者信息表(reader_info) |
| ISBN                | varchar  | 30   |      |      | 外键约束，参考图书信息表(book_info)   |
| borrow_date         | date     |      |      |      |                                       |
| due_date            | date     |      |      |      |                                       |
| return_date         | date     |      |      |      |                                       |
| fine                | decimal  | 10,2 |      |      |                                       |