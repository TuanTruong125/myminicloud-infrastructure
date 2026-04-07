CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;

-- Tạo bảng students với cấu trúc yêu cầu
CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(10) NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    dob DATE,
    major VARCHAR(50)
);

-- Chèn ít nhất 3 bản ghi mẫu (Insert)
INSERT INTO students (student_id, fullname, dob, major) VALUES 
('52300063', 'Phan Nguyen Quoc Thang', '2005-01-01', 'Software Engineering'),
('52300066', 'Nguyen Hoang Nhut Thien', '2005-07-22', 'Computer Science'),
('52300080', 'Truong Anh Tuan', '2005-02-01', 'Data Science');