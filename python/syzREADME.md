# 登录注册板块（login.py）

- **register 函数**
  
  **功能**：进行注册
  
  **参数**：name->要注册的姓名，password->要注册的密码，title->职称，phone_number->电话号码，department->系别，gender->性别，is_root->是否为管理员

  **返回值**：
  - 成功
  
  ```json
  {
    "success":True,
    "data":account
  }
  
  ```

  - 失败（代码与说明）
    - 1 :姓名为空错误
    - 2 :密码为空错误
    - 3 :姓名长度过长
    - 4 :密码长度过长
    - 10:权限设置错误
    - 20:身份长度过长
    - 21:性别不为男也不为女
    - 22:系别长度过长
    - 23:电话长度过长
    - 301:数据库操作错误
    - 401:意外错误
  
- **login函数**

  **功能**：登录

  **参数**：account->账号，password->密码

  **返回值**：
  - 成功

   ```json
  {
    "success":True,
    "data":{
      "role":role,
      "name":name
    }
  }
  
  ```

  - 失败
  
    - 1 ：用户名或密码错误
    - 301：数据库部分错误
    - 401：意外错误

# 借书还书板块（borrowbook.py）

- **borrow_book函数**
  
  **功能**：借书

  **参数**：library_card_number->借书号/账号,isbn->借书的isbn号,due_date->到期时间,begin_date->起始时间，默认为当天

  **返回值**：

  - 成功 
  
   ```json
  {
    "success":True,
    "data":{
            "library_card_number":library_card_number,
            "isbn":isbn,
            "begin_date":begin_date,
            "due_date":due_date
        }
  }
  
  ```

  - 失败
    - 1 ：isbn不存在错误
    - 2 ：library_card_number不存在错误
    - 3 ：借书超过上限错误
    - 4 ：有未交罚金或有未在时间内归还的图书
    - 5 ：重复借同一本书
    - 6 ：书籍不可借
    - 301：数据库操作错误
    - 401：意外错误

- **return_book函数**
  **功能**：还书，并提醒快过期和已经过期的书单

  **参数**：library_card_number->借书号/账号,isbn->借书的isbn号

  **返回值**：
  - 成功
  
  ```json
  {
    "success":True,
    "data":[
      [isbn,due_date,fine],
      [isbn,due_date,fine],
      ...
    ]
  }
  
  ```

  - 失败
    - 1 ：借书记录不存在错误
    - 301：数据库操作错误
    - 401：意外错误
