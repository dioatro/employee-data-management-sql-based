import hashlib
import hmac
import secrets
import time
from typing import Dict, Optional

# Supported credentials as requested:
# Username: "2026BTCS022" and "2026BCAI020"
# Password: "passwordispassword"

def hash_password(password: str, salt: str = "salt_emp_mgmt_2026") -> str:
    """Generates a secure SHA-256 hash with salt for constant-time comparison."""
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

USERS_DATABASE = {
    "2026BTCS022": {
        "username": "2026BTCS022",
        "name": "BTCS Systems Administrator",
        "email": "2026btcs022@enterprise.internal",
        "department": "Computer Science & Engineering",
        "role": "Lead Administrator",
        "badge": "ADMIN",
        "permissions": ["all", "read", "write", "delete", "export", "configure"],
        "password_hash": hash_password("passwordispassword")
    },
    "2026BCAI020": {
        "username": "2026BCAI020",
        "name": "BCAI Operations Specialist",
        "email": "2026bcai020@enterprise.internal",
        "department": "Artificial Intelligence & Computing",
        "role": "Systems Analyst",
        "badge": "ANALYST",
        "permissions": ["all", "read", "write", "delete", "export", "configure"],
        "password_hash": hash_password("passwordispassword")
    }
}

# In-memory active session store: session_token -> {username, created_at, expires_at}
SESSION_TTL_SECONDS = 86400  # 24 hours
active_sessions: Dict[str, dict] = {}

def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticates username and password securely."""
    user = USERS_DATABASE.get(username.strip())
    if not user:
        return None
    
    input_hash = hash_password(password.strip())
    if hmac.compare_digest(input_hash, user["password_hash"]):
        return {
            "username": user["username"],
            "name": user["name"],
            "email": user["email"],
            "department": user["department"],
            "role": user["role"],
            "badge": user["badge"],
            "permissions": user["permissions"]
        }
    return None

def create_session(username: str) -> str:
    """Creates a secure session token and registers session state."""
    token = secrets.token_hex(32)
    now = time.time()
    active_sessions[token] = {
        "username": username,
        "created_at": now,
        "expires_at": now + SESSION_TTL_SECONDS
    }
    return token

def get_session_user(token: Optional[str]) -> Optional[dict]:
    """Resolves session token to authenticated user profile."""
    if not token or token not in active_sessions:
        return None
    session = active_sessions[token]
    if time.time() > session["expires_at"]:
        del active_sessions[token]
        return None
    
    user_record = USERS_DATABASE.get(session["username"])
    if not user_record:
        return None

    return {
        "username": user_record["username"],
        "name": user_record["name"],
        "email": user_record["email"],
        "department": user_record["department"],
        "role": user_record["role"],
        "badge": user_record["badge"],
        "permissions": user_record["permissions"],
        "session_created": session["created_at"]
    }

def terminate_session(token: Optional[str]) -> bool:
    """Invalidates and removes session token."""
    if token and token in active_sessions:
        del active_sessions[token]
        return True
    return False
