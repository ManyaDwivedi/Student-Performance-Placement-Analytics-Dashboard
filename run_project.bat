@echo off
REM =====================================================================
REM  Student Performance & Placement Analytics - Windows Run Script
REM =====================================================================

echo ======================================================
echo  Student Performance ^& Placement Analytics
echo ======================================================
echo.

REM ---- Step 1: Check Python availability ----
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found on this system.
    echo Please install Python 3.12+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found.

REM ---- Step 2: Create virtual environment if it does not exist ----
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
) else (
    echo [OK] Virtual environment already exists.
)

REM ---- Step 3: Activate virtual environment ----
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM ---- Step 4: Install dependencies ----
echo [INFO] Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM ---- Step 5: Generate dataset if needed ----
if not exist "data\student_placement_data.csv" (
    echo [INFO] Generating dataset...
    python src\data_generator.py
) else (
    echo [OK] Raw dataset already exists.
)

REM ---- Step 6: Clean data if needed ----
if not exist "data\cleaned_student_data.csv" (
    echo [INFO] Cleaning dataset...
    python src\data_cleaning.py
) else (
    echo [OK] Cleaned dataset already exists.
)

REM ---- Step 7: Run analysis ----
echo [INFO] Running analysis and generating visualizations...
python src\analysis.py

REM ---- Step 8: Start Streamlit dashboard ----
echo [INFO] Launching Streamlit dashboard...
echo The dashboard will open at http://localhost:8501
streamlit run dashboard\app.py

pause
