import io
import csv
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Request, Response, status
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app import auth, config, crud
from app.database import db
from app.models import (
    DashboardStats,
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
    LoginRequest,
    LoginResponse,
    SystemHealth,
    UserProfile,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Employee Data Management Enterprise Dashboard",
    description="Business-focused HR and Payroll Management Platform interfacing with SQL databases.",
    version="2.0.0"
)

# Static files mount
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.on_event("startup")
def startup_event():
    """Initializes tables and seeds base records on server startup."""
    db.init_database()

# ==============================================================================
# Authentication Endpoints
# ==============================================================================

@app.post("/api/auth/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest, response: Response):
    """Authenticates user credentials and establishes a session."""
    user = auth.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please verify your Username and Password."
        )
    token = auth.create_session(user["username"])
    # Set HttpOnly session cookie
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=86400,
        samesite="lax"
    )
    return LoginResponse(
        success=True,
        token=token,
        user=UserProfile(**user),
        message="Authentication successful"
    )

@app.post("/api/auth/logout")
def logout_user(request: Request, response: Response):
    """Terminates active session and clears auth cookie."""
    token = request.cookies.get("session_token") or request.headers.get("x-session-token")
    auth.terminate_session(token)
    response.delete_cookie(key="session_token")
    return {"success": True, "message": "Logged out successfully"}

@app.get("/api/auth/me", response_model=UserProfile)
def get_current_user(request: Request):
    """Returns currently authenticated user profile."""
    token = request.cookies.get("session_token") or request.headers.get("x-session-token")
    user = auth.get_session_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or unauthenticated."
        )
    return UserProfile(**user)

# ==============================================================================
# Application & Dashboard Endpoints
# ==============================================================================

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serves the primary enterprise dashboard single-page web interface."""
    template_path = BASE_DIR / "templates" / "index.html"
    return HTMLResponse(content=template_path.read_text(encoding="utf-8"))

@app.get("/api/health", response_model=SystemHealth)
def get_system_health():
    """Returns database backend status, connection state, and live record count."""
    count_res = db.fetch_one("SELECT COUNT(*) as total FROM employee")
    total = count_res["total"] if count_res else 0
    return SystemHealth(
        database_backend=db.active_backend.upper(),
        database_name=config.MYSQL_DATABASE if db.active_backend == "mysql" else "Local SQLite Database",
        status="ONLINE",
        total_records=total
    )

@app.get("/api/stats", response_model=DashboardStats)
def get_stats():
    """Returns aggregated executive KPIs: payroll, headcount, and distribution metrics."""
    return crud.get_dashboard_stats()

@app.get("/api/departments")
def list_departments():
    """Returns a list of all distinct departments for filtering and dropdowns."""
    return {"departments": crud.get_departments()}

@app.get("/api/employees")
def list_employees(
    search: Optional[str] = Query(None, description="Search term for Name, Emp_no, or Role"),
    dept: Optional[str] = Query(None, description="Filter by department"),
    gender: Optional[str] = Query(None, description="Filter by gender (M/F/O)"),
    sort_by: str = Query("Emp_no", description="Sort field"),
    sort_order: str = Query("ASC", description="Sort direction: ASC or DESC"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Retrieves paginated, filtered, and sorted employee records."""
    offset = (page - 1) * page_size
    records, total = crud.list_employees(
        search=search,
        dept=dept,
        gender=gender,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=page_size,
        offset=offset
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return {
        "items": records,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@app.get("/api/employees/{emp_no}", response_model=EmployeeResponse)
def get_employee_by_id(emp_no: int):
    """Retrieves single employee record by Emp_no (Option 4 'R' in original CLI)."""
    record = crud.get_employee(emp_no)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with Emp_no {emp_no} was not found."
        )
    return record

@app.post("/api/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_new_employee(employee: EmployeeCreate):
    """Adds a new employee record (Option 1 in original CLI)."""
    try:
        created = crud.create_employee(employee)
        return created
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

@app.put("/api/employees/{emp_no}", response_model=EmployeeResponse)
def update_existing_employee(emp_no: int, update_data: EmployeeUpdate):
    """Configures/updates employee fields (Option 3 in original CLI)."""
    updated = crud.update_employee(emp_no, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with Emp_no {emp_no} was not found."
        )
    return updated

@app.delete("/api/employees/{emp_no}")
def delete_existing_employee(emp_no: int):
    """Removes an employee record (Option 2 in original CLI)."""
    success = crud.delete_employee(emp_no)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with Emp_no {emp_no} was not found."
        )
    return {"message": f"Employee {emp_no} removed successfully."}

@app.get("/api/export/csv")
def export_employees_csv():
    """Generates and streams an enterprise CSV export of all employees."""
    records, _ = crud.list_employees(limit=10000, offset=0)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Emp_no", "Name", "Gender", "Age", "Role", "Dept", "Salary"])
    for r in records:
        writer.writerow([r["Emp_no"], r["Name"], r["Gender"], r["Age"], r["Role"], r["Dept"], f"{r['Salary']:.2f}"])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=employees_roster.csv"}
    )
