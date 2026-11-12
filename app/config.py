import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "project")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "Employee_Data_Management")

# Engine selection: "mysql", "sqlite", or "auto" (attempts MySQL, falls back to SQLite gracefully)
DB_BACKEND = os.getenv("DB_BACKEND", "auto")

# SQLite fallback path
SQLITE_PATH = os.getenv("SQLITE_PATH", str(BASE_DIR / "employee_data.db"))

# Application server settings
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("APP_PORT", 8000))
APP_DEBUG = os.getenv("APP_DEBUG", "false").lower() in ("true", "1", "yes")
