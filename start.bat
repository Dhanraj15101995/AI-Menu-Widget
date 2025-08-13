@echo off
echo Starting AI Menu Widget...
echo.

echo Starting server...
start "Server" cmd /k "cd server && npm start"

echo Waiting 3 seconds for server to start...
timeout /t 3 /nobreak > nul

echo Starting client...
start "Client" cmd /k "cd client && npm run dev"

echo.
echo Both client and server are starting...
echo Server: http://localhost:4000
echo Client: http://localhost:5173
echo.
echo Press any key to close this window...
pause > nul
