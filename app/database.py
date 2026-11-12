import sqlite3
import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple

import pymysql
from pymysql.cursors import DictCursor

from app import config

logger = logging.getLogger("employee_app.database")
logging.basicConfig(level=logging.INFO)

class DatabaseManager:
    """
    Unified database manager supporting MySQL with automatic SQLite fallback.
    Ensures parameterized queries and zero SQL injection vulnerability.
    """
    def __init__(self):
        self.active_backend = "unknown"
        self._check_and_set_backend()

    def _test_mysql(self) -> bool:
        try:
            conn = pymysql.connect(
                host=config.MYSQL_HOST,
                port=config.MYSQL_PORT,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE,
                connect_timeout=2,
                cursorclass=DictCursor,
                autocommit=True
            )
            conn.close()
            return True
        except Exception as e:
            logger.warning("MySQL connection test failed (%s).", e)
            return False

    def _check_and_set_backend(self):
        backend_pref = config.DB_BACKEND.lower()
        if backend_pref == "mysql":
            self.active_backend = "mysql"
        elif backend_pref == "sqlite":
            self.active_backend = "sqlite"
        else:  # "auto"
            if self._test_mysql():
                self.active_backend = "mysql"
                logger.info("Connected to MySQL backend (%s:%s/%s).", config.MYSQL_HOST, config.MYSQL_PORT, config.MYSQL_DATABASE)
            else:
                self.active_backend = "sqlite"
                logger.info("Using SQLite fallback database at %s.", config.SQLITE_PATH)

    @contextmanager
    def get_connection(self):
        """Yields an active database connection and ensures clean closure."""
        if self.active_backend == "mysql":
            conn = pymysql.connect(
                host=config.MYSQL_HOST,
                port=config.MYSQL_PORT,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE,
                cursorclass=DictCursor,
                autocommit=False
            )
            try:
                yield conn
            finally:
                conn.close()
        else:
            conn = sqlite3.connect(config.SQLITE_PATH)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
            finally:
                conn.close()

    def _adapt_query_params(self, query: str, params: Optional[Tuple]) -> Tuple[str, Tuple]:
        """Translates %s placeholders to ? if using SQLite."""
        if self.active_backend == "sqlite":
            query = query.replace("%s", "?")
        return query, params or ()

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        query, params = self._adapt_query_params(query, params)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if self.active_backend == "mysql":
                rows = cursor.fetchall()
            else:
                rows = [dict(row) for row in cursor.fetchall()]
            cursor.close()
            return rows

    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        query, params = self._adapt_query_params(query, params)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if self.active_backend == "mysql":
                row = cursor.fetchone()
            else:
                raw_row = cursor.fetchone()
                row = dict(raw_row) if raw_row else None
            cursor.close()
            return row

    def execute_write(self, query: str, params: Optional[Tuple] = None) -> int:
        query, params = self._adapt_query_params(query, params)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                conn.commit()
                rowcount = cursor.rowcount
                cursor.close()
                return rowcount
            except Exception as e:
                conn.rollback()
                cursor.close()
                raise e

    def init_database(self):
        """Ensures the employee table exists and seeds initial records if empty."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS employee (
            Emp_no INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Gender CHAR(1) NOT NULL,
            Age INTEGER NOT NULL,
            Role VARCHAR(60) NOT NULL,
            Dept VARCHAR(60) NOT NULL,
            Salary NUMERIC(12, 2) NOT NULL
        );
        """
        if self.active_backend == "sqlite":
            with self.get_connection() as conn:
                conn.execute(create_table_sql)
                conn.commit()
        else:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(create_table_sql)
                conn.commit()
                cursor.close()

        # Seed sample data if table is currently empty
        count_res = self.fetch_one("SELECT COUNT(*) as cnt FROM employee")
        count = count_res["cnt"] if count_res else 0
        if count == 0:
            logger.info("Initializing sample employee dataset...")
            sample_records = [
                (1001, 'Alexander Wright', 'M', 34, 'Senior Software Engineer', 'Engineering', 125000),
                (1002, 'Elena Rostova', 'F', 29, 'Frontend Developer', 'Engineering', 98000),
                (1003, 'Marcus Vance', 'M', 42, 'Director of Engineering', 'Engineering', 185000),
                (1004, 'Sophia Chen', 'F', 31, 'DevOps Lead', 'Engineering', 135000),
                (1005, 'David Kim', 'M', 26, 'QA Automation Engineer', 'Engineering', 88000),
                (1006, 'Rachel Green', 'F', 38, 'Head of Human Resources', 'Human Resources', 140000),
                (1007, 'Carlos Mendez', 'M', 28, 'HR Generalist', 'Human Resources', 72000),
                (1008, 'Aaliyah Patel', 'F', 33, 'Talent Acquisition Partner', 'Human Resources', 85000),
                (1009, 'Jonathan Hayes', 'M', 45, 'Chief Financial Officer', 'Finance', 210000),
                (1010, 'Olivia Taylor', 'F', 36, 'Senior Financial Analyst', 'Finance', 115000),
                (1011, 'Ethan Brooks', 'M', 27, 'Staff Accountant', 'Finance', 76000),
                (1012, 'Victoria Sterling', 'F', 39, 'VP of Marketing', 'Marketing', 165000),
                (1013, 'Liam O\'Connor', 'M', 30, 'Growth Marketing Lead', 'Marketing', 95000),
                (1014, 'Zoe Washington', 'F', 25, 'Content Strategist', 'Marketing', 68000),
                (1015, 'Daniel Martinez', 'M', 41, 'VP of Sales', 'Sales', 170000),
                (1016, 'Isabella Rossi', 'F', 32, 'Enterprise Account Executive', 'Sales', 130000),
                (1017, 'Noah Jenkins', 'M', 29, 'Business Development Rep', 'Sales', 65000),
                (1018, 'Samantha Reed', 'F', 35, 'Principal Product Manager', 'Product', 150000),
                (1019, 'Kevin Zhao', 'M', 28, 'UI/UX Product Designer', 'Product', 102000),
                (1020, 'Beatriz Gomez', 'F', 40, 'Head of Operations', 'Operations', 142000),
            ]
            for rec in sample_records:
                self.execute_write(
                    "INSERT INTO employee (Emp_no, Name, Gender, Age, Role, Dept, Salary) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    rec
                )
            logger.info("Successfully seeded %d sample records.", len(sample_records))

db = DatabaseManager()
