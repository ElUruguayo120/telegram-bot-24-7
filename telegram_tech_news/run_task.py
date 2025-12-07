#!/usr/bin/env python3
"""
Wrapper para ejecutar el bot una vez (para tareas programadas como PythonAnywhere)
Ejecuta el bot por un tiempo limitado para que PythonAnywhere pueda ejecutarlo cada hora
"""
import os
import sys
import time
import traceback

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de entorno desde .env si existe
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Importar después de configurar variables de entorno
from news_bot import (
    TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, TELEGRAM_CHANNEL,
    CHECK_INTERVAL, POLL_INTERVAL, ADMIN_ID,
    log, load_history, process_updates, fetch_and_post_news
)

# Ejecutar el bot por un tiempo limitado (55 minutos)
START_TIME = time.time()
MAX_RUNTIME = 55 * 60  # 55 minutos

def run_limited():
    """Ejecuta el bot por tiempo limitado para tareas programadas"""
    
    log("=" * 50)
    log("🤖 Bot 5.0: Scheduled Task Mode (PythonAnywhere)")
    log("=" * 50)

    if not TELEGRAM_BOT_TOKEN:
        log("ERROR: TELEGRAM_BOT_TOKEN environment variable not set!")
        return

    if not GEMINI_API_KEY:
        log("WARNING: GEMINI_API_KEY not set. AI features disabled.")
        
    log(f"Bot Token: {TELEGRAM_BOT_TOKEN[:10]}...")
    log(f"Channel: {TELEGRAM_CHANNEL}")
    log(f"Max runtime: {int(MAX_RUNTIME/60)} minutes")
    log("=" * 50)
    
    history = load_history()
    log(f"👑 System Admin: {ADMIN_ID}")
    
    # Forzar check de noticias al inicio
    last_news_check = time.time() - CHECK_INTERVAL
    
    # Ejecutar por tiempo limitado
    while time.time() - START_TIME < MAX_RUNTIME:
        try:
            current_time = time.time()
            
            # 1. Poll for chat messages
            process_updates(history)
            
            # 2. Check news
            if current_time - last_news_check >= CHECK_INTERVAL:
                log(f"Time for news check. Last check was {int(current_time - last_news_check)} seconds ago.")
                fetch_and_post_news(history)
                last_news_check = current_time
            
            time.sleep(POLL_INTERVAL)
            
            # Verificar tiempo restante
            elapsed = time.time() - START_TIME
            remaining = MAX_RUNTIME - elapsed
            if elapsed >= MAX_RUNTIME:
                log(f"⏰ Maximum runtime reached ({int(MAX_RUNTIME/60)} minutes). Exiting gracefully...")
                break
            elif int(remaining) % 300 == 0 and remaining < 600:
                log(f"⏱️ Remaining time: {int(remaining/60)} minutes")
                
        except KeyboardInterrupt:
            log("Bot stopped by user")
            break
        except Exception as e:
            log(f"Critical Loop Error: {e}")
            log(f"Traceback: {traceback.format_exc()}")
            log("Retrying in 10 seconds...")
            time.sleep(10)
    
    log("=" * 50)
    log("✅ Task completed. Bot will restart in next scheduled run.")
    log("=" * 50)

if __name__ == "__main__":
    run_limited()

# https://Eluruguayo1900.pythonanywhere.com

