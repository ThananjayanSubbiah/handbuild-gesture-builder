@echo off
cd /d "%~dp0"
where py >nul 2>nul && (set "PY=py -3.11") || (set "PY=python")
if not exist .venv ( %PY% -m venv .venv || goto :error )
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt || goto :error
python main.py
pause
exit /b
:error
echo Setup failed. Install Python 3.11 and check your internet connection.
pause
exit /b 1
