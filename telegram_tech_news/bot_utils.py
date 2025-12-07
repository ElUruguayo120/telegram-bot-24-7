
import json
import time
import re
import threading
import requests
import traceback
from datetime import datetime, timedelta
import google.generativeai as genai
from .bot_config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL, GEMINI_API_KEY, 
    HISTORY_FILE, LOG_FILE, BASE_DIR
)

GENAI_AVAILABLE = True
try:
    import google.generativeai as genai
except ImportError:
    GENAI_AVAILABLE = False

HISTORY_LOCK = threading.Lock()

def log(message):
    """Log messages to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    except:
        pass

def load_history():
    """Load history JSON"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                data.setdefault("urls", [])
                data.setdefault("messages", {})
                data.setdefault("alarms", {})
                data.setdefault("paused", False)
                data.setdefault("last_offset", 0)
                data["urls"] = set(data.get("urls", []))
                return data
        except Exception as e:
            log(f"Error loading history: {e}")
    return {"urls": set(), "messages": {}, "alarms": {}, "paused": False, "last_offset": 0}

def save_history(history):
    """Save history JSON"""
    try:
        to_save = dict(history)
        if isinstance(to_save.get("urls"), set):
            to_save["urls"] = list(to_save["urls"])
        
        with HISTORY_LOCK:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(to_save, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"Error saving history: {e}")

def clean_html_for_telegram(text):
    """Clean text for Telegram HTML parse mode"""
    if not text: return ""
    text = re.sub(r'</?p[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?(html|body|head|span|img|iframe|script|style)[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text

def markdown_to_html_style(text):
    """Convert Markdown to Telegram HTML"""
    if not text: return ""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    text = re.sub(r'^\s*[\-\*]\s+(.*)$', r'• \1', text, flags=re.MULTILINE)
    return text

def send_to_telegram(message, chat_id=None, silent=False):
    """Send message to Telegram"""
    target = chat_id if chat_id else TELEGRAM_CHANNEL
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    cleaned_message = clean_html_for_telegram(message)
    
    payload = {
        "chat_id": target,
        "text": cleaned_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
        "disable_notification": silent
    }
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.ok
    except Exception as e:
        log(f"Error sending to Telegram: {e}")
        return False

def chat_with_gemini(user_text, context=""):
    """Get response from Gemini"""
    if not GEMINI_API_KEY:
        return "IA no disponible (API Key missing)"
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        models_to_try = [
            'gemini-2.0-flash-lite',
            'gemini-2.0-flash',
            'gemini-2.5-flash',
            'gemini-1.5-flash'
        ]
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                prompt = f"{context}\n\nUsuario: {user_text}"
                response = model.generate_content(prompt)
                if response:
                    return response.text
            except Exception as e:
                # log(f"Model {model_name} failed: {e}")
                continue
                
        return "Lo siento, mis neuronas están agotadas (Error de IA)."
    except Exception as e:
        return f"Error IA: {e}"

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
