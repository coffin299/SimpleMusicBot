@echo off
chcp 65001 >nul
title ARONA Music Bot STARTER

set "VENV_DIR=.venv"

echo ================================
echo ARONA Music Bot STARTER
echo ================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found on PATH.
    echo [ERROR] Install Python and try again.
    pause
    exit /b 1
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [INFO] Creating virtual environment in "%VENV_DIR%"...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create the virtual environment.
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created.
    echo.
) else (
    echo [INFO] Virtual environment already exists.
    echo.
)

echo [INFO] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate the virtual environment.
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated.
echo.

echo [INFO] Installing / updating packages from requirements.txt...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [ERROR] Failed to upgrade pip.
    pause
    exit /b 1
)
python -m pip install -U -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install packages from requirements.txt.
    pause
    exit /b 1
)
echo [SUCCESS] Packages are ready.
echo.

if not exist "config.yaml" (
    echo [WARN] config.yaml was not found.
    echo [WARN] Copy config.default.yaml to config.yaml and set your bot token.
    echo.
)

echo ================================
echo Starting ARONA...
echo ================================
echo.
python bot.py
set "EXIT_CODE=%errorlevel%"

echo.
echo ================================
echo ARONA has stopped.
echo ================================
if not "%EXIT_CODE%"=="0" (
    echo [WARN] Bot exited with code %EXIT_CODE%.
)
pause
exit /b %EXIT_CODE%
