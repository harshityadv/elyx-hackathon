@echo off
echo Setting up Elyx Healthcare Dashboard for Windows...

echo Creating virtual environment...
python -m venv elyx_venv

echo Activating virtual environment...
call elyx_venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete!
echo.
echo To run the application:
echo 1. Start Ollama: ollama serve
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
pause
