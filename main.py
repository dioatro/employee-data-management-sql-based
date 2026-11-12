#!/usr/bin/env python3
"""
Main Application Launcher for Employee Data Management System.
Supports both modern Web Dashboard and fixed CLI terminal mode.

Usage:
    python3 main.py          # Starts the web dashboard at http://localhost:8000
    python3 main.py --cli    # Starts the terminal interactive CLI
"""
import sys
import argparse
import uvicorn
from app import config

def main():
    parser = argparse.ArgumentParser(description="Employee Data Management Suite")
    parser.add_argument("--cli", action="store_true", help="Launch interactive CLI menu instead of web server")
    parser.add_argument("--host", default=config.APP_HOST, help="Host address for web server")
    parser.add_argument("--port", type=int, default=config.APP_PORT, help="Port for web server")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    args = parser.parse_args()

    if args.cli:
        from cli import menu
        menu()
    else:
        print(f"================================================================")
        print(f"🚀 Starting Employee Data Management Enterprise Dashboard")
        print(f"🌐 Access Dashboard at: http://{args.host}:{args.port}")
        print(f"📚 API Documentation at: http://{args.host}:{args.port}/docs")
        print(f"================================================================")
        uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()
