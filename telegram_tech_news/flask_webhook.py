
import os
import threading
import time
from flask import Flask, request, Response
import requests
from .bot_config import TELEGRAM_BOT_TOKEN, ADMIN_ID, TELEGRAM_CHANNEL
from .bot_utils import (
    log, chat_with_gemini, markdown_to_html_style, send_to_telegram,
    load_history, save_history, format_time
)

app = Flask(__name__)

# --- Helper Routes ---

@app.route('/')
def index():
    return "🤖 Bot Activo 24/7 (Webhook Mode)"

@app.route('/set_webhook')
def set_webhook():
    """Call this route once to tell Telegram where to send messages"""
    # Assuming the app is hosted at <your-username>.pythonanywhere.com
    host = request.host_url
    if 'localhost' in host:
        return "❌ Cannot set webhook to localhost. Deploy to Server first."
    
    webhook_url = f"{host}webhook"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}"
    
    try:
        r = requests.get(url)
        return f"Webhook setup result: {r.text}"
    except Exception as e:
        return f"Error: {e}"

# --- Main Webhook Route ---

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = request.get_json()
        
        # Run processing in a separate thread so we don't block Telegram logic
        # Note: In strict Serverless, threads might be killed, but for Flask App it's okay for short tasks
        t = threading.Thread(target=process_update, args=(update,))
        t.start()
        
        return Response('ok', status=200)
    else:
        return '403 Forbidden', 403

def process_update(update):
    try:
        if "message" not in update:
            return

        message = update["message"]
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        
        # User Info
        first_name = message.get("from", {}).get("first_name", "User")
        
        if not text:
            return

        text_lower = text.lower()
        history = load_history()

        # --- Commands ---

        if text_lower == "/start":
            send_to_telegram(f"👋 Hola {first_name}! Soy tu bot Tech con IA.\n\nComandos:\n/alarma [tiempo]\n/last (Noticias)\nEscríbeme para hablar con IA.", chat_id)
            return

        if text_lower == "/last":
            # Show last 5 news
             articles = list(history.get("messages", {}).items())[-5:]
             if articles:
                msg = "📰 <b>Últimas Noticias:</b>\n\n"
                for url, data in reversed(articles):
                    title = data.get("title", "?")[:50]
                    msg += f"• <a href='{url}'>{title}</a>\n"
                send_to_telegram(msg, chat_id)
             else:
                send_to_telegram("No hay noticias recientes.", chat_id)
             return

        if text_lower.startswith("/alarma"):
            # Simple threaded alarm
            # Note: This thread dies if the WebWorker is recycled. 
            parts = text.split()
            if len(parts) > 1:
                try:
                    # Simple seconds parsing for demo
                    arg = parts[1]
                    if 'm' in arg: seconds = int(arg.replace('m','')) * 60
                    elif 's' in arg: seconds = int(arg.replace('s',''))
                    else: seconds = int(arg) * 60 # Default minutes
                    
                    send_to_telegram(f"⏰ Alarma puesta en {format_time(seconds)}.", chat_id)
                    
                    def alarm_thread(sec, cid):
                        time.sleep(sec)
                        send_to_telegram("🔔 <b>¡RIIIING!</b> Tu alarma ha sonado.", cid)
                    
                    t = threading.Thread(target=alarm_thread, args=(seconds, chat_id))
                    t.start()
                except:
                    send_to_telegram("Uso: /alarma 5m (5 minutos)", chat_id)
            return

        # --- AI Chat ---
        
        # Don't reply in channels unless tagged (optional logic, simplfed here for DM)
        # If private chat:
        if message.get("chat", {}).get("type") == "private":
            send_to_telegram("💬 Pensando...", chat_id, silent=True) # Typing indicator simulation
            
            context = f"Tu nombre es TechBot. Hablas con {first_name}."
            response = chat_with_gemini(text, context)
            formatted = markdown_to_html_style(response)
            
            send_to_telegram(formatted, chat_id)

    except Exception as e:
        log(f"Webhook error: {e}")

if __name__ == '__main__':
    # Local dev run
    app.run(debug=True, port=5000)
