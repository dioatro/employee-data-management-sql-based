from typing import Any, Dict, List, Optional, Tuple
from app.database import db
from app.models import EmployeeCreate, EmployeeUpdate, DashboardStats, DepartmentSummary

def list_employees(
    search: Optional[str] = None,
    dept: Optional[str] = None,
    gender: Optional[str] = None,
    sort_by: str = "Emp_no",
    sort_order: str = "ASC",
    limit: int = 100,
    offset: int = 0
) -> Tuple[List[Dict[str, Any]], int]:
    """Retrieves paginated and filtered employee records with total count."""
    valid_sort_columns = {"Emp_no", "Name", "Gender", "Age", "Role", "Dept", "Salary"}
    if sort_by not in valid_sort_columns:
        sort_by = "Emp_no"
    sort_order = "DESC" if sort_order.upper() == "DESC" else "ASC"

    where_clauses = []
    params: List[Any] = []

    if search:
        where_clauses.append("(Name LIKE %s OR CAST(Emp_no AS CHAR) LIKE %s OR Role LIKE %s)")
        term = f"%{search}%"
        params.extend([term, term, term])

    if dept and dept != "ALL":
        where_clauses.append("Dept = %s")
        params.append(dept)

    if gender and gender != "ALL":
        where_clauses.append("Gender = %s")
        params.append(gender)

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    # Total matching count
    count_sql = f"SELECT COUNT(*) as total FROM employee {where_sql}"
    count_res = db.fetch_one(count_sql, tuple(params))
    total = count_res["total"] if count_res else 0

    # Data fetch
    query = f"""
        SELECT Emp_no, Name, Gender, Age, Role, Dept, Salary 
        FROM employee 
        {where_sql} 
        ORDER BY {sort_by} {sort_order} 
        LIMIT %s OFFSET %s
    """
    fetch_params = tuple(params + [limit, offset])
    rows = db.fetch_all(query, fetch_params)
    return rows, total

def get_employee(emp_no: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single employee record by ID."""
    query = "SELECT Emp_no, Name, Gender, Age, Role, Dept, Salary FROM employee WHERE Emp_no = %s"
    return db.fetch_one(query, (emp_no,))

def create_employee(emp: EmployeeCreate) -> Dict[str, Any]:
    """Creates a new employee record after checking for duplicate Emp_no."""
    existing = get_employee(emp.Emp_no)
    if existing:
        raise ValueError(f"Employee with Emp_no {emp.Emp_no} already exists.")

    query = """
        INSERT INTO employee (Emp_no, Name, Gender, Age, Role, Dept, Salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    db.execute_write(
        query,
        (emp.Emp_no, emp.Name, emp.Gender, emp.Age, emp.Role, emp.Dept, emp.Salary)
    )
    return get_employee(emp.Emp_no)

def update_employee(emp_no: int, update_data: EmployeeUpdate) -> Optional[Dict[str, Any]]:
    """Updates selected fields of an existing employee record."""
    existing = get_employee(emp_no)
    if not existing:
        return None

    fields_to_update = []
    params = []
    data_dict = update_data.model_dump(exclude_unset=True)

    if not data_dict:
        return existing

    for field, val in data_dict.items():
        fields_to_update.append(f"{field} = %s")
        params.append(val)

    params.append(emp_no)
    set_clause = ", ".join(fields_to_update)
    query = f"UPDATE employee SET {set_clause} WHERE Emp_no = %s"

    db.execute_write(query, tuple(params))
    return get_employee(emp_no)

def delete_employee(emp_no: int) -> bool:
    """Deletes an employee record by Emp_no."""
    query = "DELETE FROM employee WHERE Emp_no = %s"
    rows_affected = db.execute_write(query, (emp_no,))
    return rows_affected > 0

def get_departments() -> List[str]:
    """Retrieves unique department names."""
    rows = db.fetch_all("SELECT DISTINCT Dept FROM employee ORDER BY Dept ASC")
    return [r["Dept"] for r in rows if r.get("Dept")]

def get_dashboard_stats() -> DashboardStats:
    """Calculates executive dashboard metrics and breakdown distributions."""
    total_res = db.fetch_one("""
        SELECT 
            COUNT(*) as total_employees,
            COALESCE(SUM(Salary), 0) as total_payroll,
            COALESCE(AVG(Salary), 0) as average_salary,
            COUNT(DISTINCT Dept) as departments_count
        FROM employee
    """)

    # Gender distribution
    gender_rows = db.fetch_all("""
        SELECT Gender, COUNT(*) as count 
        FROM employee 
        GROUP BY Gender
    """)
    gender_dist = {r["Gender"]: r["count"] for r in gender_rows}

    # Department breakdown
    dept_rows = db.fetch_all("""
        SELECT 
            Dept,
            COUNT(*) as count,
            COALESCE(AVG(Salary), 0) as avg_salary,
            COALESCE(SUM(Salary), 0) as total_payroll
        FROM employee 
        GROUP BY Dept 
        ORDER BY count DESC
    """)
    dept_dist = [
        DepartmentSummary(
            Dept=r["Dept"],
            count=r["count"],
            avg_salary=round(float(r["avg_salary"]), 2),
            total_payroll=round(float(r["total_payroll"]), 2)
        )
        for r in dept_rows
    ]

    # Salary ranges bracket analysis
    salary_rows = db.fetch_all("""
        SELECT 
            CASE 
                WHEN Salary < 75000 THEN '< $75k'
                WHEN Salary BETWEEN 75000 AND 100000 THEN '$75k - $100k'
                WHEN Salary BETWEEN 100001 AND 150000 THEN '$100k - $150k'
                ELSE '> $150k'
            END as salary_tier,
            COUNT(*) as count
        FROM employee
        GROUP BY salary_tier
    """)
    salary_ranges = {r["salary_tier"]: r["count"] for r in salary_rows}

    return DashboardStats(
        total_employees=total_res["total_employees"] if total_res else 0,
        total_payroll=round(float(total_res["total_payroll"] or 0), 2) if total_res else 0.0,
        average_salary=round(float(total_res["average_salary"] or 0), 2) if total_res else 0.0,
        departments_count=total_res["departments_count"] if total_res else 0,
        gender_distribution=gender_dist,
        department_distribution=dept_dist,
        salary_ranges=salary_ranges
    )
