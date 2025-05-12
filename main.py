"""
Telegram Bot для обмена криптовалюты LTC

Этот скрипт запускает Telegram бота для обмена LTC с системой ролей, заявками и реферальной программой.
Бот может быть запущен напрямую через командную строку:
python bot.py
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

@app.route('/')
def index():
    return jsonify({
        "status": "running",
        "message": "BudgetBuddy Telegram Bot Server is running. The bot is active and can be used via Telegram."
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "app": "BudgetBuddy Telegram Bot"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)