@echo off
echo ========================================
echo Attendance System Launcher
echo ========================================

:: Check if venv exists
if not exist "venv" (
    echo Virtual environment not found! Run scripts/setup_venv.py first.
    pause
    exit /b
)

:: Activate virtual environment
call venv\Scripts\activate

:: Run the application
echo Starting Smart Attendance System...
python src/main.py
pause
