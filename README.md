# employee-data-management-sql-based

This is a school project named "Employee Data Management"

-------------------------------------------------------

## 1. Create Database

Open your MySQL prompt or terminal and execute the following command to create the database:

```sql
CREATE DATABASE Employee_Data_Management;
```

---

## 2. Select the Database

After creating the database, select it to use:

```sql
USE Employee_Data_Management;
```

---

## 3. Create Employee Table

```sql
CREATE TABLE employee(Emp_no INTEGER, Name CHAR(25),Gender CHAR(1),Age INT(2),Role CHAR(30),Dept CHAR(30),Salary INTEGER);
```

---

## 4. Verify Table Creation

To make sure the table has been created correctly, run:

```sql
DESCRIBE employee;
```

You should see all the columns with their respective types.

---

