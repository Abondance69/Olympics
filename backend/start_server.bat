@echo off
echo.
echo ============================================================
echo   Demarrage du serveur Backend Olympics
echo ============================================================
echo.

cd /d "%~dp0"
call ..\.venv\Scripts\activate.bat
python app.py

pause
