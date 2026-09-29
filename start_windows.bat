@echo off
if not exist .venv\Scripts\python.exe (
  echo Virtual environment not found. Run setup_windows.ps1 first.
  pause
  exit /b 1
)
.venv\Scripts\python.exe run.py
