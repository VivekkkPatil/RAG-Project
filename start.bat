@echo off
call venv\Scripts\activate
set PYTHONPATH=.
start cmd /k "uvicorn backend.main:app --reload"
timeout /t 3
start cmd /k "streamlit run frontend/app.py"