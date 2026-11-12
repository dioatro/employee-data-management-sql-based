# Employee Data Management — Enterprise Suite & Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite-4479A1.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A complete, business-focused Employee & Payroll Management platform featuring a high-productivity **Web Dashboard**, modern **FastAPI** REST backend, resilient **MySQL/SQLite** database engine, and a hardened terminal **CLI**.

---

## 🌟 Features Overview

- **Secure Authentication & Login Portal**:
  - Pre-configured institutional credentials (`2026BTCS022` and `2026BCAI020`).
  - Salted SHA-256 password hashing with constant-time comparison (`hmac.compare_digest`).
  - Cryptographically secure 256-bit session tokens stored via `HttpOnly`, `SameSite=Lax` cookies.
  - Interactive credential chips and show/hide password toggle.
- **User Profile & Security Clearance**:
  - Live authenticated profile pill in the executive top header.
  - Detailed Profile Modal displaying assigned department, institutional email, clearance role, and granted system permissions.
- **One-Click Sign Out**: Instant server-side session termination and cookie invalidation.
- **Executive KPI Dashboard**: Live tracking of workforce headcount, cumulative annual payroll, mean salary, and departmental breakdown.
- **Full CRUD Management**:
  - **Create**: Add employees with field validation (`Emp_no`, `Name`, `Gender`, `Age`, `Role`, `Dept`, `Salary`).
  - **Read**: Dynamic roster table with real-time debounced text search, department & gender filtering, multi-column sorting, and pagination.
  - **Single Lookup**: Search single employee profiles by ID (Option 4 'R' parity).
  - **Update**: Modal configuration of employee fields (Age, Role, Department, Salary, Name).
  - **Delete**: Safe deletion with confirmation modal (Option 2 parity).
- **Business Intelligence**: Department distribution progress bars and demographic representation analysis.
- **Enterprise Reporting**: One-click streaming CSV export (`/api/export/csv`) of the entire employee dataset.
- **Database Resilience**: Built for **MySQL** with automatic fallback to **SQLite** if MySQL is not yet configured or offline.
- **Security Hardened**: 100% parameterized SQL queries (immune to SQL injection), no recursion call stack overflow, and deterministic cursor lifecycle management.
- **Dual Interface**: Run the high-productivity Web Dashboard or launch the terminal CLI.

---

## 🏗️ Architecture

```
employee-data-management-sql-based/
├── app/
│   ├── config.py           # Configuration and environment variable loader
│   ├── auth.py             # Authentication, password hashing, and session management
│   ├── database.py         # Unified MySQL / SQLite database engine manager
│   ├── models.py           # Pydantic data schemas & validation
│   ├── crud.py             # Parameterized SQL business logic
│   ├── main.py             # FastAPI REST API routes & static file server
│   ├── static/             # Frontend assets
│   │   ├── css/dashboard.css
│   │   └── js/dashboard.js
│   └── templates/
│       └── index.html      # Responsive executive web interface
├── scripts/
│   ├── schema.sql          # MySQL database schema DDL
│   ├── sample_data.sql     # Enterprise seed data (20 employees)
│   └── seed.py             # Python database seeding tool
├── cli.py                  # Fixed, secure terminal CLI
├── main.py                 # Unified launcher (starts Web or CLI)
├── requirements.txt        # Python package dependencies
└── .env.example            # Environment configuration template
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Web Dashboard
```bash
python3 main.py
```
Then navigate to:
👉 **[http://localhost:8000](http://localhost:8000)**

#### 🔑 Pre-Configured Portal Credentials:
| Username | Password | Role / Department | Clearance |
|---|---|---|---|
| `2026BTCS022` | `passwordispassword` | BTCS Systems Administrator &bull; CSE | `ADMIN` (Full Access) |
| `2026BCAI020` | `passwordispassword` | BCAI Operations Specialist &bull; AI & Computing | `ANALYST` (Full Access) |

Interactive REST API documentation (Swagger UI) is available at:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

### 3. Launch the Terminal CLI (Optional)
If you prefer the terminal interface:
```bash
python3 main.py --cli
# or directly
python3 cli.py
```

---

## 🗄️ MySQL Database Setup

### A. Run MySQL Schema & Sample Data
Open your MySQL terminal or client and execute:
```bash
mysql -u root -p < scripts/schema.sql
mysql -u root -p < scripts/sample_data.sql
```

Alternatively, use the Python seeder tool:
```bash
python3 scripts/seed.py --engine mysql
```

### B. Environment Variables
Create a `.env` file (or copy from `.env.example`):
```env
DB_BACKEND=auto
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=Employee_Data_Management
```

> **Note**: If MySQL is not running, the application will automatically initialize the local fallback database (`employee_data.db`) so you can preview and test all features instantly without configuration.

---

## 📊 Database Schema Details

```sql
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
);

CREATE INDEX idx_employee_dept ON employee(Dept);
CREATE INDEX idx_employee_role ON employee(Role);
CREATE INDEX idx_employee_salary ON employee(Salary);
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/login` | Authenticate user credentials and create session |
| `POST` | `/api/auth/logout` | Invalidate active session and clear auth cookie |
| `GET` | `/api/auth/me` | Fetch currently logged-in user profile |
| `GET` | `/api/health` | System health check, active DB backend, and total records |
| `GET` | `/api/stats` | Executive KPIs (Headcount, Payroll, Average Salary, Demographics) |
| `GET` | `/api/departments` | List distinct departments |
| `GET` | `/api/employees` | Search, filter, sort, and paginate employee records |
| `GET` | `/api/employees/{id}` | Retrieve single employee record by ID |
| `POST` | `/api/employees` | Add a new employee |
| `PUT` | `/api/employees/{id}` | Update existing employee details |
| `DELETE` | `/api/employees/{id}` | Remove employee from database |
| `GET` | `/api/export/csv` | Stream full employee roster as CSV |

---

## 🛡️ Key Improvements from Legacy Version

1. **SQL Injection Eliminated**: Replaced vulnerable `str.format()` string concatenation with parameterized query placeholders (`%s`).
2. **Infinite Recursion Fixed**: Replaced recursive function calls (`menu()` calling itself) with an iterative event loop.
3. **Resource Leak Fixed**: Cursor and connection lifecycles are strictly managed using context managers and `try...finally` blocks.
4. **Data Validation**: Strict schema enforcement through Pydantic models (age bounds, gender enumeration, positive salaries).
5. **Modern Authentication**: Salted cryptographic password validation with session state management.
6. **REST API**: Standardized JSON endpoints for easy integration with HRIS or third-party enterprise tools.
