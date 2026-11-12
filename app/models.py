from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

class EmployeeBase(BaseModel):
    Emp_no: int = Field(..., description="Unique employee identifier", ge=1)
    Name: str = Field(..., min_length=1, max_length=100, description="Full name")
    Gender: str = Field(..., max_length=1, description="M, F, or O")
    Age: int = Field(..., ge=18, le=100, description="Age between 18 and 100")
    Role: str = Field(..., min_length=1, max_length=60, description="Job role")
    Dept: str = Field(..., min_length=1, max_length=60, description="Department")
    Salary: float = Field(..., ge=0, description="Base annual or monthly salary")

    @field_validator("Gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        v_upper = v.upper()
        if v_upper not in ("M", "F", "O"):
            raise ValueError("Gender must be 'M', 'F', or 'O'")
        return v_upper

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    Name: Optional[str] = Field(None, min_length=1, max_length=100)
    Gender: Optional[str] = Field(None, max_length=1)
    Age: Optional[int] = Field(None, ge=18, le=100)
    Role: Optional[str] = Field(None, min_length=1, max_length=60)
    Dept: Optional[str] = Field(None, min_length=1, max_length=60)
    Salary: Optional[float] = Field(None, ge=0)

    @field_validator("Gender")
    @classmethod
    def validate_gender(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v_upper = v.upper()
        if v_upper not in ("M", "F", "O"):
            raise ValueError("Gender must be 'M', 'F', or 'O'")
        return v_upper

class EmployeeResponse(EmployeeBase):
    pass

class DepartmentSummary(BaseModel):
    Dept: str
    count: int
    avg_salary: float
    total_payroll: float

class DashboardStats(BaseModel):
    total_employees: int
    total_payroll: float
    average_salary: float
    departments_count: int
    gender_distribution: Dict[str, int]
    department_distribution: List[DepartmentSummary]
    salary_ranges: Dict[str, int]

class SystemHealth(BaseModel):
    database_backend: str
    database_name: str
    status: str
    total_records: int

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username / User ID")
    password: str = Field(..., min_length=1, description="Account password")

class UserProfile(BaseModel):
    username: str
    name: str
    email: str
    department: str
    role: str
    badge: str
    permissions: List[str]
    session_created: Optional[float] = None

class LoginResponse(BaseModel):
    success: bool
    token: str
    user: UserProfile
    message: str

