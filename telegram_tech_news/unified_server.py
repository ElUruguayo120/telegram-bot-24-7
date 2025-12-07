
import os
import time
import threading
import logging
from flask import Flask, request, Response
from apscheduler.schedulers.background import BackgroundScheduler
from .bot_config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL, 
    TELEGRAM_BOT_TOKEN as BOT_TOKEN # Alias
)
from .bot_utils import (
    log, load_history, save_history, send_to_telegram, 
    chat_with_gemini, markdown_to_html_style
)
from .rss_job import fetch_and_post_news

# --- Configuration ---
PORT = int(os.environ.get("PORT", 5000))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "") # Optional: Auto-setup webhook

# --- Log Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Flask App (The Server) ---
app = Flask(__name__)

@app.route('/')
def home():
    return f"🟢 SERVIDOR ACTIVO | Bot: TechNews | Estado: 200 OK"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint for Telegram Webhook"""
    if request.method == 'POST':
        update = request.get_json()
        threading.Thread(target=process_update_async, args=(update,)).start()
        return Response('ok', status=200)
    return '403 Forbidden', 403

def process_update_async(update):
    """Process update in background thread"""
    try:
        if "message" in update:
            msg = update["message"]
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "")
            first_name = msg.get("from", {}).get("first_name", "User")
            
            if not text: return

            # Simple logic (expandable)
            if text == "/start":
                send_to_telegram(f"👋 Hola {first_name}, servidor 24/7 activo.", chat_id)
            elif text.startswith("/"):
                pass # Other commands
            elif msg.get("chat", {}).get("type") == "private":
                # AI Chat
                send_to_telegram("💬 ...", chat_id, silent=True)
                resp = chat_with_gemini(text, f"Usuario: {first_name}")
                send_to_telegram(markdown_to_html_style(resp), chat_id)

    except Exception as e:
        logger.error(f"Error processing update: {e}")

# --- Background Tasks (The Heart) ---
def start_scheduler():
    """Starts the 24/7 scheduler for News"""
    scheduler = BackgroundScheduler()
    # Ejecutar RSS cada 1 hora
    scheduler.add_job(func=fetch_and_post_news, trigger="interval", minutes=60)
    # Ejecutar Keep-Alive ping cada 15 min (opcional)
    scheduler.start()
    logger.info("⏰ Scheduler iniciado: RSS News monitorizando...")

# --- Main Entry Point ---
if __name__ == "__main__":
    # If running locally
    start_scheduler()
    app.run(host="0.0.0.0", port=PORT)
else:
    # If running via Gunicorn (Production)
    start_scheduler()
