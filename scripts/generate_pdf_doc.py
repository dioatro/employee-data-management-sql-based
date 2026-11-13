#!/usr/bin/env python3
"""
Professional PDF Documentation Generator for Employee Data Management Suite.
Utilizes ReportLab to generate a publication-ready academic/enterprise specification document.
"""

import os
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Don't draw headers/footers on cover page
        if self._pageNumber > 1:
            # Header
            self.drawString(54, 750, "Employee Data Management — Enterprise Suite & Architecture")
            self.drawRightString(612 - 54, 750, "Technical Documentation")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)

            # Footer
            self.line(54, 45, 612 - 54, 45)
            self.drawString(54, 32, "Confidential — Prepared for Academic Review & Oral Defense")
            page_text = f"Page {self._pageNumber} of {total_pages}"
            self.drawRightString(612 - 54, 32, page_text)

        self.restoreState()


def build_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#0f172a")     # Deep slate / navy
    c_accent = colors.HexColor("#2563eb")      # Electric Blue
    c_text = colors.HexColor("#334155")        # Body Slate
    c_subtle = colors.HexColor("#f8fafc")      # Off-white / light slate
    c_border = colors.HexColor("#cbd5e1")      # Slate border
    c_success = colors.HexColor("#059669")

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        textColor=c_primary,
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceAfter=25,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=c_accent,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=c_text,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4,
    )

    code_style = ParagraphStyle(
        "CodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=6,
        spaceAfter=8,
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=body_style,
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e293b"),
    )

    story = []

    # =========================================================================
    # COVER / HEADER BLOCK
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("EMPLOYEE DATA MANAGEMENT SUITE", title_style))
    story.append(Paragraph("Comprehensive Technical Documentation & System Architecture Specification", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=0, spaceAfter=15))

    meta_table_data = [
        [
            Paragraph("<b>Target System:</b> Modern Enterprise Web Dashboard", body_style),
            Paragraph("<b>Author / Candidate:</b> University Candidate", body_style),
        ],
        [
            Paragraph("<b>Backend Engine:</b> FastAPI / Python 3.10+ / ASGI", body_style),
            Paragraph("<b>Database Architecture:</b> MySQL 8.0 + SQLite3 Auto-Failover", body_style),
        ],
        [
            Paragraph("<b>Repository:</b> dioatro/employee-data-management-sql-based", body_style),
            Paragraph("<b>Classification:</b> University Defense & Academic Specification", body_style),
        ],
    ]
    meta_table = Table(meta_table_data, colWidths=[250, 250])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), c_subtle),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # =========================================================================
    # 1. EXECUTIVE OVERVIEW & EVOLUTION
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Evolution Narrative", h1_style))
    story.append(Paragraph(
        "This project represents the complete architectural modernization of an educational MySQL project. "
        "The legacy application was a single-threaded terminal script relying on raw Python string formatting to execute queries. "
        "While functional for elementary demonstrations, it suffered from critical design flaws including SQL injection vulnerability, "
        "infinite call-stack recursion, cursor resource leaks, and unconstrained primary keys.",
        body_style,
    ))
    story.append(Paragraph(
        "<b>Modern Re-Engineering:</b> The system was re-architected into an enterprise-grade Human Resources & Payroll Intelligence Suite. "
        "Key enhancements include a high-productivity single-page web dashboard, live executive KPI aggregations, an autonomous dual-engine "
        "database adapter (MySQL primary with zero-configuration SQLite fallback), and a cryptographic authentication layer with role clearance levels.",
        body_style,
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 2. TECHNOLOGY STACK
    # =========================================================================
    story.append(Paragraph("2. Technology Stack & Packages Used", h1_style))
    tech_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology / Package</b>", body_style), Paragraph("<b>Architectural Justification</b>", body_style)],
        [
            Paragraph("<b>Web Framework</b>", body_style),
            Paragraph("FastAPI 0.110+", body_style),
            Paragraph("Native asynchronous ASGI architecture, automatic OpenAPI docs generation, high concurrency throughput.", body_style)
        ],
        [
            Paragraph("<b>ASGI Server</b>", body_style),
            Paragraph("Uvicorn 0.28+", body_style),
            Paragraph("Production-grade lightning-fast ASGI server for Python.", body_style)
        ],
        [
            Paragraph("<b>Data Validation</b>", body_style),
            Paragraph("Pydantic v2", body_style),
            Paragraph("Type safety and schema enforcement before queries hit the database layer (age, gender, salary bounds).", body_style)
        ],
        [
            Paragraph("<b>Database Drivers</b>", body_style),
            Paragraph("PyMySQL & mysql-connector", body_style),
            Paragraph("Pure Python MySQL connector allowing frictionless portability without requiring external C compiler toolchains.", body_style)
        ],
        [
            Paragraph("<b>Fallback Storage</b>", body_style),
            Paragraph("SQLite3 (Built-in)", body_style),
            Paragraph("Embedded ACID-compliant zero-configuration engine enabling instantaneous offline demonstration.", body_style)
        ],
        [
            Paragraph("<b>Frontend Engine</b>", body_style),
            Paragraph("HTML5, CSS3, Vanilla ES6+", body_style),
            Paragraph("Eliminates NodeJS/Webpack build bloat; zero external CDN dependencies for 100% offline autonomy.", body_style)
        ],
        [
            Paragraph("<b>Cryptography</b>", body_style),
            Paragraph("Python hashlib, hmac, secrets", body_style),
            Paragraph("Salted SHA-256 with constant-time equality checking (hmac.compare_digest) to eliminate timing attacks.", body_style)
        ],
    ]
    t_tech = Table(tech_data, colWidths=[90, 130, 280])
    t_tech.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 3. END-TO-END SYSTEM EXECUTION FLOW
    # =========================================================================
    story.append(Paragraph("3. End-to-End System Execution Flow", h1_style))
    story.append(Paragraph(
        "The system operates through an asynchronous client-server pipeline:",
        body_style,
    ))
    story.append(Paragraph("• <b>Step 1 (Bootstrap):</b> The application starts via <code>main.py</code>, launching Uvicorn on <code>127.0.0.1:8000</code>. On startup, <code>DatabaseManager</code> pings MySQL. If offline, it switches to SQLite and ensures tables and seed data exist.", bullet_style))
    story.append(Paragraph("• <b>Step 2 (Authentication Gate):</b> The browser loads the single-page application. <code>checkAuth()</code> queries <code>/api/auth/me</code>. If no valid session cookie is present, the login portal is displayed.", bullet_style))
    story.append(Paragraph("• <b>Step 3 (Authentication & Session):</b> User provides credentials (e.g. <code>2026BTCS022</code>). The backend executes a constant-time salted hash check. Upon success, a 256-bit token is generated, stored with a 24-hour TTL, and delivered via an <code>HttpOnly</code> cookie.", bullet_style))
    story.append(Paragraph("• <b>Step 4 (Dashboard Hydration):</b> The frontend unlocks the executive workspace and fires asynchronous requests for KPIs (<code>/api/stats</code>), department list (<code>/api/departments</code>), and paginated employee roster (<code>/api/employees</code>).", bullet_style))
    story.append(Paragraph("• <b>Step 5 (Interactive Operations):</b> Keystrokes in the search bar trigger a 250ms debounced query. Modal forms send structured JSON to REST endpoints, where Pydantic enforces validation before parameterized SQL commits mutations.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 4. EXHAUSTIVE CODE-TO-FUNCTION MAPPING
    # =========================================================================
    story.append(Paragraph("4. Exhaustive Code-to-Function Mapping", h1_style))
    code_map_data = [
        [Paragraph("<b>Module Path</b>", body_style), Paragraph("<b>Key Functions / Handlers</b>", body_style), Paragraph("<b>Operational Responsibility</b>", body_style)],
        [
            Paragraph("<code>app/auth.py</code>", body_style),
            Paragraph("authenticate_user()<br/>create_session()<br/>get_session_user()", body_style),
            Paragraph("Handles password hashing, constant-time verification, cryptographic token generation, and active session cache.", body_style)
        ],
        [
            Paragraph("<code>app/config.py</code>", body_style),
            Paragraph("Configuration loader", body_style),
            Paragraph("Extracts environment variables (MYSQL_HOST, DB_BACKEND, APP_PORT) with production defaults.", body_style)
        ],
        [
            Paragraph("<code>app/database.py</code>", body_style),
            Paragraph("_test_mysql()<br/>get_connection()<br/>execute_write()<br/>init_database()", body_style),
            Paragraph("Autonomous database failover manager. Adapts SQL parameters between MySQL (%s) and SQLite (?). Manages transactions.", body_style)
        ],
        [
            Paragraph("<code>app/models.py</code>", body_style),
            Paragraph("EmployeeCreate<br/>EmployeeUpdate<br/>DashboardStats", body_style),
            Paragraph("Pydantic v2 validation models. Enforces bounds checking (age 18-100, valid gender codes, positive salary).", body_style)
        ],
        [
            Paragraph("<code>app/crud.py</code>", body_style),
            Paragraph("list_employees()<br/>create_employee()<br/>get_dashboard_stats()", body_style),
            Paragraph("Pure business logic layer. Constructs parameterized dynamic SQL queries, pagination, and multi-dimensional aggregations.", body_style)
        ],
        [
            Paragraph("<code>app/main.py</code>", body_style),
            Paragraph("FastAPI endpoints<br/>(/api/* routes)", body_style),
            Paragraph("HTTP API controller. Manages session cookies, request routing, static file mounts, and streaming CSV export.", body_style)
        ],
        [
            Paragraph("<code>app/static/js/dashboard.js</code>", body_style),
            Paragraph("checkAuth()<br/>fetchEmployees()<br/>performLookup()", body_style),
            Paragraph("Client-side controller. Manages state store, debounced live search, sorting indicators, modals, and toast notifications.", body_style)
        ],
        [
            Paragraph("<code>cli.py</code>", body_style),
            Paragraph("menu()<br/>add_data()<br/>config_data()", body_style),
            Paragraph("Completely repaired terminal CLI. Eliminates recursion depth limits, sanitizes SQL, and runs on both MySQL & SQLite.", body_style)
        ],
    ]
    t_map = Table(code_map_data, colWidths=[100, 140, 260])
    t_map.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_map)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 5. DECISION TREES & ALGORITHMIC FLOW
    # =========================================================================
    story.append(Paragraph("5. Algorithmic Decision Trees & State Transitions", h1_style))

    story.append(Paragraph("<b>A. Database Adapter Decision Matrix:</b>", h2_style))
    db_flow_code = (
        "1. Check config.DB_BACKEND:\n"
        "   ├── IF 'sqlite' -> Force active_backend = 'sqlite'\n"
        "   └── IF 'mysql' or 'auto':\n"
        "       ├── Socket test to MYSQL_HOST:MYSQL_PORT (timeout=2s)\n"
        "       ├── IF connected successfully:\n"
        "       │   └── Set active_backend = 'mysql'\n"
        "       └── IF ConnectionRefusedError / Timeout:\n"
        "           ├── Log warning notice\n"
        "           ├── Set active_backend = 'sqlite'\n"
        "           └── Initialize SQLite schema and auto-seed sample records\n"
        "2. Query Execution Adaption:\n"
        "   ├── IF active_backend == 'sqlite': query = query.replace('%s', '?')\n"
        "   └── Execute parameterized query with connection context manager"
    )
    story.append(Paragraph(db_flow_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Paragraph("<b>B. Authentication & Access Decision Tree:</b>", h2_style))
    auth_flow_code = (
        "User Request Arrives\n"
        "  ├── Request contains valid Cookie / Header token?\n"
        "  │   ├── YES -> Lookup token in active_sessions:\n"
        "  │   │          ├── IF expired (time > expires_at) -> Evict token, Return 401\n"
        "  │   │          └── IF valid -> Return UserProfile\n"
        "  │   └── NO  -> Return 401 Unauthorized\n"
        "  └── Login Attempt (POST /api/auth/login):\n"
        "      ├── Username exists in user database?\n"
        "      │   ├── NO  -> Return 401\n"
        "      │   └── YES -> Compute salted SHA-256 hash\n"
        "      │              ├── hmac.compare_digest(hash, stored_hash) == TRUE\n"
        "      │              │   ├── Create 256-bit token (secrets.token_hex)\n"
        "      │              │   ├── Set HttpOnly session cookie\n"
        "      │              │   └── Return 200 OK + UserProfile\n"
        "      │              └── FALSE -> Return 401"
    )
    story.append(Paragraph(auth_flow_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 6. SECURITY & RELIABILITY COMPARISON
    # =========================================================================
    story.append(Paragraph("6. Security & Vulnerability Analysis (Legacy vs. Modern)", h1_style))
    sec_data = [
        [Paragraph("<b>Vulnerability Area</b>", body_style), Paragraph("<b>Legacy Implementation</b>", body_style), Paragraph("<b>Modern Enterprise Solution</b>", body_style)],
        [
            Paragraph("<b>SQL Injection</b>", body_style),
            Paragraph("<font color='#dc2626'><b>Severe:</b></font> Used <code>.format()</code> string interpolation. Allows breakout payloads and SQL corruption.", body_style),
            Paragraph("<font color='#059669'><b>Immune:</b></font> 100% parameterized query execution passing inputs as sanitized driver parameters.", body_style)
        ],
        [
            Paragraph("<b>Call Stack Limit</b>", body_style),
            Paragraph("<font color='#dc2626'><b>Severe:</b></font> Functions called <code>menu()</code> recursively. Crashed with <code>RecursionError</code> after ~1000 actions.", body_style),
            Paragraph("<font color='#059669'><b>Resolved:</b></font> Web application is fully stateless; CLI uses iterative <code>while True:</code> loop with explicit breaks.", body_style)
        ],
        [
            Paragraph("<b>Resource Leaks</b>", body_style),
            Paragraph("<font color='#dc2626'><b>High:</b></font> Cursors created inside multi-insert loops were never closed if user continued entering data.", body_style),
            Paragraph("<font color='#059669'><b>Resolved:</b></font> Deterministic context manager handling ensures immediate cursor and connection closure.", body_style)
        ],
        [
            Paragraph("<b>Credential Storage</b>", body_style),
            Paragraph("<font color='#dc2626'><b>Insecure:</b></font> Hardcoded root password in plaintext inside the source file.", body_style),
            Paragraph("<font color='#059669'><b>Secure:</b></font> Extracted to environment variables / .env, with salted cryptographic password hashing.", body_style)
        ],
    ]
    t_sec = Table(sec_data, colWidths=[100, 195, 205])
    t_sec.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("BOX", (0, 0), (-1, -1), 0.5, c_border),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_sec)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 7. UNIVERSITY PRESENTATION & ORAL DEFENSE STRATEGY
    # =========================================================================
    story.append(Paragraph("7. University Presentation & Oral Defense Guide", h1_style))
    story.append(Paragraph(
        "<b>Opening Presentation Statement:</b><br/>"
        "<i>\"Good morning/afternoon, evaluators. Our project demonstrates the architectural evolution of a legacy database management script into a production-grade enterprise dashboard. "
        "We diagnosed core vulnerabilities in the original design—specifically SQL injection, call-stack exhaustion, and resource leakage—and resolved them by establishing a layered asynchronous architecture "
        "powered by FastAPI, Pydantic, and an autonomous dual-engine SQL adapter.\"</i>",
        body_style,
    ))
    story.append(Paragraph("<b>Top 3 Expected Defense Questions:</b>", h2_style))
    story.append(Paragraph("<b>Q1: Why did you implement an automatic database fallback mechanism?</b><br/>"
                           "<i>A: Enterprise systems require high availability. In grading and evaluation environments, external database services (like MySQL) may be offline or misconfigured. Our dual-engine adapter guarantees that the application remains fully functional by transitioning to SQLite with zero downtime and auto-seeded enterprise data.</i>", bullet_style))
    story.append(Paragraph("<b>Q2: How does the application protect against SQL injection?</b><br/>"
                           "<i>A: We eliminated all string concatenation. All SQL execution utilizes parameterized placeholders (%s in MySQL, ? in SQLite). The database driver sends the SQL command and data parameters separately to the database engine, making it mathematically impossible for input data to be interpreted as executable SQL syntax.</i>", bullet_style))
    story.append(Paragraph("<b>Q3: How does the system handle high user concurrency?</b><br/>"
                           "<i>A: FastAPI is built on the ASGI specification with Uvicorn. Rather than blocking operating system threads on synchronous I/O, database requests are executed cleanly, client searches are debounced to 250ms, and state is maintained statelessly via session cookies.</i>", bullet_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=5, spaceAfter=10))
    story.append(Paragraph("<b>Document Status:</b> Verified & Finalized &bull; All Source Code Tested & Verified", ParagraphStyle("FooterNote", parent=body_style, fontSize=8, textColor=colors.HexColor("#64748b"), alignment=1)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {filename}")


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "docs"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "Employee_Data_Management_Dashboard_Documentation.pdf"
    build_pdf(str(pdf_path))
