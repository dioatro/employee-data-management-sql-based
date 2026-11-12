#!/usr/bin/env python3
"""
Modernized, Secure CLI for Employee Data Management.
Fixes all previous issues:
 - Eliminates RecursionError by using an iterative event loop.
 - Fixes SQL injection with parameterized SQL queries.
 - Fixes UnboundLocalError and ensures deterministic cursor cleanup.
 - Connects securely via the database abstraction layer (MySQL + SQLite fallback).
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import db

def menu():
    db.init_database()
    while True:
        print("\n==============================================")
        print("  Employee Data Management System (CLI)       ")
        print(f"  Backend: {db.active_backend.upper()}")
        print("==============================================")
        print(" 1. Add Employee Data")
        print(" 2. Remove Employee Data")
        print(" 3. Configure Employee Data")
        print(" 4. View Data")
        print(" 5. Exit")
        print("----------------------------------------------")
        
        raw_choice = input("Select an option (1-5): ").strip()
        if not raw_choice.isdigit():
            print("Invalid input! Please enter a number between 1 and 5.")
            continue

        choice = int(raw_choice)
        if choice == 1:
            add_data()
        elif choice == 2:
            remove_data()
        elif choice == 3:
            config_data()
        elif choice == 4:
            view_data()
        elif choice == 5:
            print("Exiting... See You Next Time!")
            break
        else:
            print("Invalid Option! Please select between 1 and 5.")

def add_data():
    while True:
        try:
            emp_no = int(input("Enter Employee's no.: ").strip())
            # Check for duplicate
            existing = db.fetch_one("SELECT Emp_no FROM employee WHERE Emp_no = %s", (emp_no,))
            if existing:
                print(f"Error: Employee with ID {emp_no} already exists.")
                break

            name = input("Enter Employee's Name: ").strip()
            gender = input("Enter gender (M/F/O): ").strip().upper()
            if gender not in ('M', 'F', 'O'):
                print("Invalid gender! Please enter M, F, or O.")
                continue

            age = int(input("Enter Employee's age: ").strip())
            role = input("Enter the Employee's role: ").strip()
            dept = input("Enter Department: ").strip()
            salary = float(input("Enter Employee's Salary: ").strip())

            # Parameterized Query
            db.execute_write(
                "INSERT INTO employee (Emp_no, Name, Gender, Age, Role, Dept, Salary) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (emp_no, name, gender, age, role, dept, salary)
            )
            print(f"Employee #{emp_no} added successfully!")

        except ValueError as e:
            print(f"Input error: {e}")

        ch = input("Wanna enter more employee data? (Y/N): ").strip().upper()
        if ch != 'Y':
            break

def remove_data():
    try:
        del_emp = int(input("Enter Employee No. to be removed: ").strip())
        rows_affected = db.execute_write(
            "DELETE FROM employee WHERE Emp_no = %s",
            (del_emp,)
        )
        if rows_affected == 0:
            print("Employee No. not found!")
        else:
            print(f"Employee #{del_emp} removed successfully!")
    except ValueError:
        print("Invalid input! Employee ID must be an integer.")

def config_data():
    try:
        upg_emp = int(input("Enter Employee No. to be configured: ").strip())
        existing = db.fetch_one("SELECT * FROM employee WHERE Emp_no = %s", (upg_emp,))
        if not existing:
            print("Employee not found!")
            return

        print(f"Current Record: {existing}")
        upg_item = input("Fields that can be updated:\n Age (A)\n Role (R)\n Department (D)\n Salary (S)\n Enter the Field: ").strip().upper()

        if upg_item == 'A':
            age = int(input("Enter new Age: ").strip())
            db.execute_write("UPDATE employee SET Age = %s WHERE Emp_no = %s", (age, upg_emp))
            print("Age updated successfully!")
        elif upg_item == 'R':
            role = input("Enter new Role: ").strip()
            db.execute_write("UPDATE employee SET Role = %s WHERE Emp_no = %s", (role, upg_emp))
            print("Role updated successfully!")
        elif upg_item == 'D':
            dept = input("Enter new Department: ").strip()
            db.execute_write("UPDATE employee SET Dept = %s WHERE Emp_no = %s", (dept, upg_emp))
            print("Department updated successfully!")
        elif upg_item == 'S':
            salary = float(input("Enter new Salary: ").strip())
            db.execute_write("UPDATE employee SET Salary = %s WHERE Emp_no = %s", (salary, upg_emp))
            print("Salary updated successfully!")
        else:
            print("Field Not Recognized!")

    except ValueError:
        print("Invalid numerical input.")

def view_data():
    choice = input("Do you want to view the whole table (T) or single row (R)?: ").strip().upper()
    if choice == 'T':
        rows = db.fetch_all("SELECT * FROM employee ORDER BY Emp_no ASC")
        if not rows:
            print("Table is currently empty.")
            return
        print("\n" + "=" * 90)
        print(f"{'Emp_no':<8} {'Name':<22} {'Gender':<8} {'Age':<6} {'Role':<22} {'Dept':<16} {'Salary':<10}")
        print("-" * 90)
        for r in rows:
            print(f"{r['Emp_no']:<8} {r['Name']:<22} {r['Gender']:<8} {r['Age']:<6} {r['Role']:<22} {r['Dept']:<16} ${r['Salary']:<10.2f}")
        print("=" * 90)
    elif choice == 'R':
        try:
            emp_no = int(input("Enter Employee No.: ").strip())
            r = db.fetch_one("SELECT * FROM employee WHERE Emp_no = %s", (emp_no,))
            if r:
                print("\n--- Employee Details ---")
                for key, val in r.items():
                    print(f"  {key}: {val}")
            else:
                print("Employee not found!")
        except ValueError:
            print("Invalid input! Employee ID must be a number.")
    else:
        print("Invalid Selection! Enter 'T' or 'R'.")

if __name__ == "__main__":
    menu()
