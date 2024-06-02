-- ɾ�����ݿ⣨������ڣ�
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'LibraryDB')
BEGIN
    DROP DATABASE LibraryDB;
END
GO
create database LibraryDB;
-- ʹ�����ݿ�
USE LibraryDB;

/*����*/
-- ������½��
CREATE TABLE login_table (
    Account INT PRIMARY KEY IDENTITY(1,1),
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
	foreign key(library_card_number) references login_table(Account)
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


/* �������� */
-- �������Ա
INSERT INTO login_table (Password, Role)
VALUES ( 'admin_password', 1);

-- �������
INSERT INTO login_table (Password, Role)
VALUES ( 'reader_password', 0);

INSERT INTO reader_info (library_card_number, name, gender, title, available_quantity, borrowed_quantity, department, contact_number)
VALUES (2, '����', '��', 'ѧ��', 10, 0, '�������ѧ�뼼��', '12345678901');

-- ����ͼ��
INSERT INTO book_info (ISBN, book_title, publisher, author, total_quantity, available_quantity, is_borrowable)
VALUES  
('978-3-16-148410-0', 'ͼ��1', '������A', '����A', 5, 5, 1),
('978-0-12-345678-9', 'ͼ��2', '������B', '����B', 3, 3, 1),
('978-1-23-456789-0', 'ͼ��3', '������C', '����C', 4, 4, 1),
('978-9-87-654321-0', 'ͼ��4', '������D', '����D', 2, 2, 1),
('978-4-56-789123-0', 'ͼ��5', '������E', '����E', 6, 6, 1);

-- ���������Ϣ
INSERT INTO borrow_info (library_card_number, ISBN, borrow_date, due_date, return_date, fine)
VALUES 
(2, '978-3-16-148410-0', '2023-01-01', '2023-01-15', '2023-01-14', 0.00),
(2, '978-0-12-345678-9', '2023-02-01', '2023-02-15', NULL, 0.00);

