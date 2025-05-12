@echo off
echo Telegram Bot Startup Script (Windows)
echo ===================================

:: Setup environment variables (uncomment and set if needed)
:: set TELEGRAM_BOT_TOKEN=your_bot_token_here
:: set DATABASE_URL=sqlite:///crypto_exchange.db

:: Check if Python is installed
python --version >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found. Please install Python 3.6 or later.
    pause
    exit /b 1
)

:: Check Python version
for /f "tokens=2" %%V in ('python --version 2^>^&1') do set PY_VERSION=%%V
for /f "tokens=1,2 delims=." %%A in ("%PY_VERSION%") do (
    set PY_MAJOR=%%A
    set PY_MINOR=%%B
)

if %PY_MAJOR% LSS 3 (
    echo Error: Python 3.6 or later is required. Found Python %PY_VERSION%.
    pause
    exit /b 1
)
if %PY_MAJOR% EQU 3 if %PY_MINOR% LSS 6 (
    echo Error: Python 3.6 or later is required. Found Python %PY_VERSION%.
    pause
    exit /b 1
)

:: Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

:: Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
)

:: Start the bot
echo Starting the bot...
python bot.py

:: If the bot exits, show a message
echo Bot has stopped. To restart, run this script again.
pause
