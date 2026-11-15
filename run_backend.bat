@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
)

echo Starting GeoLens at http://127.0.0.1:5000
echo Do not change the port. If it is busy, stop the other process first.
python app.py
if errorlevel 1 (
    echo.
    echo Backend failed to start. See the error above.
    pause
)
