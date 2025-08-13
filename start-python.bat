@echo off
echo Starting AI Menu Widget with Python Backend...
echo.

echo Starting Python backend...
start "Python Backend" cmd /k "cd python-backend && python main.py"

echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak > nul

echo Starting React frontend...
start "React Frontend" cmd /k "cd client && npm run dev"

echo.
echo Both services are starting...
echo Python Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo React Frontend: http://localhost:5173
echo.
echo Press any key to close this window...
pause > nul
