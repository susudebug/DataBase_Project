DROP DATABASE LibraryDB

CREATE DATABASE LibraryDB

-- ʹ�����ݿ�
USE LibraryDB;

/*����*/
-- ������½��
CREATE TABLE login_table
  (
     Account  INT PRIMARY KEY,
     Password NVARCHAR(50) NOT NULL,
     Role     INT NOT NULL DEFAULT 0
  );

-- ����ͼ����Ϣ��
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

-- ����������Ϣ��
CREATE TABLE reader_info
  (
     library_card_number INT PRIMARY KEY,
     name                VARCHAR(50) NOT NULL,
     gender              VARCHAR(10) CHECK (gender IN ('��', 'Ů')),
     title               VARCHAR(50),
     available_quantity  INT,
     borrowed_quantity   INT,
     department          VARCHAR(100),
     contact_number      VARCHAR(15),
     FOREIGN KEY(library_card_number) REFERENCES login_table(Account)
  );

-- ����������Ϣ��
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
