-- 删除数据库（如果存在）
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'LibraryDB')
BEGIN
    DROP DATABASE LibraryDB;
END
GO
create database LibraryDB;
-- 使用数据库
USE LibraryDB;

/*建表*/
-- 创建登陆表
CREATE TABLE login_table (
    Account INT PRIMARY KEY IDENTITY(1,1),
    Password NVARCHAR(50) NOT NULL,
    Role INT NOT NULL DEFAULT 0 
);


-- 创建图书信息表
CREATE TABLE book_info (
    ISBN VARCHAR(30) PRIMARY KEY,
    book_title VARCHAR(100) NOT NULL,
    publisher VARCHAR(50),
    author VARCHAR(50),
    total_quantity INT,
    available_quantity INT,
    is_borrowable BIT CHECK (is_borrowable IN (0, 1))
);


-- 创建读者信息表
CREATE TABLE reader_info (
    library_card_number INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('男', '女')),
    title VARCHAR(50),
    available_quantity INT,
    borrowed_quantity INT,
    department VARCHAR(100),
    contact_number VARCHAR(15),
	foreign key(library_card_number) references login_table(Account)
);


-- 创建借阅信息表
CREATE TABLE borrow_info (
    borrow_id INT PRIMARY KEY IDENTITY(1,1),
    library_card_number INT,
    ISBN VARCHAR(30),
    borrow_date DATE,
    due_date DATE,
    return_date DATE,
    fine DECIMAL(10, 2),
    FOREIGN KEY (library_card_number) REFERENCES reader_info(library_card_number),
    FOREIGN KEY (ISBN) REFERENCES book_info(ISBN)
);


/* 插入数据 */
-- 插入管理员
INSERT INTO login_table (Password, Role)
VALUES ( 'admin_password', 1);

-- 插入读者
INSERT INTO login_table (Password, Role)
VALUES ( 'reader_password', 0);

INSERT INTO reader_info (library_card_number, name, gender, title, available_quantity, borrowed_quantity, department, contact_number)
VALUES (2, '张三', '男', '学生', 10, 0, '计算机科学与技术', '12345678901');

-- 插入图书
INSERT INTO book_info (ISBN, book_title, publisher, author, total_quantity, available_quantity, is_borrowable)
VALUES  
('978-3-16-148410-0', '图书1', '出版社A', '作者A', 5, 5, 1),
('978-0-12-345678-9', '图书2', '出版社B', '作者B', 3, 3, 1),
('978-1-23-456789-0', '图书3', '出版社C', '作者C', 4, 4, 1),
('978-9-87-654321-0', '图书4', '出版社D', '作者D', 2, 2, 1),
('978-4-56-789123-0', '图书5', '出版社E', '作者E', 6, 6, 1);

-- 插入借阅信息
INSERT INTO borrow_info (library_card_number, ISBN, borrow_date, due_date, return_date, fine)
VALUES 
(2, '978-3-16-148410-0', '2023-01-01', '2023-01-15', '2023-01-14', 0.00),
(2, '978-0-12-345678-9', '2023-02-01', '2023-02-15', NULL, 0.00);

