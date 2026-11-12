#!/usr/bin/env python3
"""
Seed Script: Populates MySQL or fallback SQLite with 20 realistic employee records.
Usage:
    python3 scripts/seed.py [--engine mysql|sqlite|auto]
"""
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import db
from app import config

SAMPLE_EMPLOYEES = [
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

def main():
    parser = argparse.ArgumentParser(description="Seed employee database.")
    parser.add_argument("--engine", choices=["mysql", "sqlite", "auto"], default=None, help="Database engine target")
    args = parser.parse_args()

    if args.engine:
        config.DB_BACKEND = args.engine
        db._check_and_set_backend()

    print(f"Targeting backend: {db.active_backend.upper()}")
    db.init_database()

    # Clear and insert fresh records
    print("Resetting table records...")
    db.execute_write("DELETE FROM employee")

    for rec in SAMPLE_EMPLOYEES:
        db.execute_write(
            "INSERT INTO employee (Emp_no, Name, Gender, Age, Role, Dept, Salary) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            rec
        )
    print(f"Successfully seeded {len(SAMPLE_EMPLOYEES)} employee records into {db.active_backend.upper()} database.")

if __name__ == "__main__":
    main()
