drop database LibraryDB
create database LibraryDB
-- ʹ�����ݿ�
USE LibraryDB;

/*����*/
-- ������½��
CREATE TABLE login_table (
    Account NVARCHAR(50) PRIMARY KEY ,
    Password NVARCHAR(50) NOT NULL,
    Role INT NOT NULL DEFAULT 0 
);


-- ����ͼ����Ϣ��
CREATE TABLE book_info (
    ISBN VARCHAR(30) PRIMARY KEY,
    book_title VARCHAR(100) NOT NULL,
    publisher VARCHAR(50),
    author VARCHAR(50),
    total_quantity INT,
    available_quantity INT,
    is_borrowable BIT CHECK (is_borrowable IN (0, 1))
);


-- ����������Ϣ��
CREATE TABLE reader_info (
    library_card_number INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('��', 'Ů')),
    title VARCHAR(50),
    available_quantity INT,
    borrowed_quantity INT,
    department VARCHAR(100),
    contact_number VARCHAR(15),
	Account NVARCHAR(50),
	foreign key(Account) references login_table(Account)
);


-- ����������Ϣ��
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


--���Ĭ�Ϲ���Ա
INSERT INTO login_table (Account, password, role)VALUES ('admin_user', 'admin_pass', 1);
INSERT INTO login_table (Account, password, role)VALUES ('reader_user', 'reader_pass', 0);
--���ͼ��
INSERT INTO book_info (ISBN, book_title, publisher, author, total_quantity, available_quantity, is_borrowable)
VALUES ('9781491991732', 'Flask Web Development', 'Reilly Media', 'Miguel Grinberg', 10, 8, 1),
('9781593276034', 'Python Crash Course', 'No Starch Press', 'Eric Matthes', 15, 10, 1),
('9780596520830', 'Learning SQL', 'Reilly Media', 'Alan Beaulieu', 12, 5, 1),
('9781449355739', 'Learning Python', 'Reilly Media', 'Mark Lutz', 20, 20, 1),
('9780134685991', 'Effective Java', 'Addison-Wesley', 'Joshua Bloch', 8, 2, 1);

--��Ӷ���
INSERT INTO reader_info (library_card_number, name, gender, title, available_quantity, borrowed_quantity, department, contact_number, Account)
VALUES (1, '����', '��', '����', 10, 3, '�������ѧ�뼼��', '12345678901', 'reader_user');



