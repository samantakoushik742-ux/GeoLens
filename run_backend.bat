@echo off
setlocal
cd /d "%~dp0"

if not defined HOST set "HOST=0.0.0.0"
if not defined PORT set "PORT=5000"

if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
)

echo Starting GeoLens backend on %HOST%:%PORT%
echo Local URL: http://127.0.0.1:%PORT%
python app.py
if errorlevel 1 (
    echo.
    echo Backend failed to start. See the error above.
    pause
)
