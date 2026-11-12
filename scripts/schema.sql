-- ============================================================================
-- Database Schema for Employee Data Management
-- Compatible with MySQL 5.7+ / MySQL 8.0+ / MariaDB
-- ============================================================================

CREATE DATABASE IF NOT EXISTS Employee_Data_Management
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE Employee_Data_Management;

-- Drop table if exists to ensure clean migration when needed
DROP TABLE IF EXISTS employee;

CREATE TABLE employee (
    Emp_no INT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Gender CHAR(1) NOT NULL,
    Age INT NOT NULL,
    Role VARCHAR(60) NOT NULL,
    Dept VARCHAR(60) NOT NULL,
    Salary DECIMAL(12, 2) NOT NULL,
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (Emp_no),
    CONSTRAINT chk_gender CHECK (Gender IN ('M', 'F', 'O')),
    CONSTRAINT chk_age CHECK (Age >= 18 AND Age <= 100),
    CONSTRAINT chk_salary CHECK (Salary >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Performance Indexes for search and aggregation
CREATE INDEX idx_employee_dept ON employee(Dept);
CREATE INDEX idx_employee_role ON employee(Role);
CREATE INDEX idx_employee_salary ON employee(Salary);
