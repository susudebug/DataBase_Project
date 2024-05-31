DROP DATABASE LibraryDB

CREATE DATABASE LibraryDB

-- 使用数据库
USE LibraryDB;

/*建表*/
-- 创建登陆表
CREATE TABLE login_table
  (
     Account  INT PRIMARY KEY,
     Password NVARCHAR(50) NOT NULL,
     Role     INT NOT NULL DEFAULT 0
  );

-- 创建图书信息表
CREATE TABLE book_info
  (
     ISBN               VARCHAR(30) PRIMARY KEY,
     book_title         VARCHAR(100) NOT NULL,
     publisher          VARCHAR(50),
     author             VARCHAR(50),
     total_quantity     INT,
     available_quantity INT,
     is_borrowable      BIT CHECK (is_borrowable IN (0, 1))
  );

-- 创建读者信息表
CREATE TABLE reader_info
  (
     library_card_number INT PRIMARY KEY,
     name                VARCHAR(50) NOT NULL,
     gender              VARCHAR(10) CHECK (gender IN ('男', '女')),
     title               VARCHAR(50),
     available_quantity  INT,
     borrowed_quantity   INT,
     department          VARCHAR(100),
     contact_number      VARCHAR(15),
     FOREIGN KEY(library_card_number) REFERENCES login_table(Account)
  );

-- 创建借阅信息表
CREATE TABLE borrow_info
  (
     borrow_id           INT PRIMARY KEY IDENTITY(1, 1),
     library_card_number INT,
     ISBN                VARCHAR(30),
     borrow_date         DATE,
     due_date            DATE,
     return_date         DATE,
     fine                DECIMAL(10, 2),
     FOREIGN KEY (library_card_number) REFERENCES reader_info(library_card_number),
     FOREIGN KEY (ISBN) REFERENCES book_info(ISBN)
  ); 
