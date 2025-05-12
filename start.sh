#!/bin/bash

# Start script for the Telegram Bot (Linux/Unix)

# Setup environment variables (uncomment and set if needed)
# export TELEGRAM_BOT_TOKEN="your_bot_token_here"
# export DATABASE_URL="sqlite:///crypto_exchange.db"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if python is available
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Error: Python not found. Please install Python 3.6 or later."
    exit 1
fi

# Check Python version
PY_VERSION=$($PYTHON --version 2>&1 | awk '{print $2}')
PY_MAJOR=$(echo $PY_VERSION | cut -d. -f1)
PY_MINOR=$(echo $PY_VERSION | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 6 ]); then
    echo "Error: Python 3.6 or later is required. Found Python $PY_VERSION."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    $PYTHON -m pip install -r requirements.txt
fi

# Start the bot
echo "Starting the bot..."
$PYTHON bot.py

# If the bot exits, show a message
echo "Bot has stopped. To restart, run this script again."
