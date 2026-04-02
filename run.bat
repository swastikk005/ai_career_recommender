@echo off
echo Starting AI Career Recommendation System...

echo Starting Backend...
start cmd /k "cd backend && venv\Scripts\activate && python main.py"

echo Starting Frontend...
start cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting up.
echo Once ready:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
pause
