@echo off
REM CareLine Clinic - Startup Script

echo.
echo ================================
echo  CareLine Clinic Application
echo ================================
echo.

REM Start Backend
echo Starting Backend (FastAPI on port 8001)...
start cmd /k "cd BAACK && python -m uvicorn main:app --reload --port 8001"

REM Wait 2 seconds
timeout /t 2 /nobreak

REM Start Frontend
echo Starting Frontend (Live Server on port 5500)...
start cmd /k "cd FRONT && python -m http.server 5500"

REM Info message
echo.
echo ✓ Backend: http://127.0.0.1:8001
echo ✓ Frontend: http://127.0.0.1:5500
echo ✓ Swagger Docs: http://127.0.0.1:8001/docs
echo.
echo Login with:
echo   Username: admin
echo   Password: password
echo.
echo Press any key to exit setup...
pause
