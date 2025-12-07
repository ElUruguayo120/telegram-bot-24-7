#!/usr/bin/env python3
"""
Telegram Tech News Bot - Funcional y completo
"""
import os
import sys
import json
import time
import re
import threading
import uuid
import traceback
from datetime import datetime, timedelta
from pathlib import Path
import keep_alive  # Importar el servidor web simple

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except:
    PYDUB_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except:
    REQUESTS_AVAILABLE = False

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except:
    FEEDPARSER_AVAILABLE = False

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except:
    GENAI_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except:
    MATPLOTLIB_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except:
    BEAUTIFULSOUP_AVAILABLE = False

# Cargar variables de entorno desde .env
SCRIPT_DIR = Path(__file__).parent
env_file = SCRIPT_DIR / ".env"
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL = "@Portal_tech2"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CHECK_INTERVAL = 3600
POLL_INTERVAL = 0.5
POST_DELAY = 1
ADMIN_ID = 701604375

RSS_FEEDS = [
    "https://www.xataka.com/index.xml",
    "https://www.genbeta.com/index.xml",
    "https://www.applesfera.com/index.xml",
]

ACTIVE_ALARM_TIMERS = {}
HISTORY_FILE = SCRIPT_DIR / "posted_articles.json"
LOG_FILE = SCRIPT_DIR / "bot.log"
HISTORY_LOCK = threading.Lock()

def log(message):
    """Log messages"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    except:
        pass

def load_history():
    """Load history"""
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
    """Save history"""
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
    """
    Clean text for Telegram HTML parse mode.
    Telegram only supports: <b>, <i>, <u>, <s>, <a>, <code>, <pre>
    We must escape <, >, & in content, but preserve valid tags.
    Strategy: 
    1. Replace unsupported tags with "" or newlines
    2. Ensure valid tags are well-formed (simple regex approach)
    """
    if not text:
        return ""
        
    # 1. Remove unsupported tags common in RSS (p, div, span, etc)
    # Replace <p> and <br> with newlines
    text = re.sub(r'</?p[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # Remove other common structural tags
    text = re.sub(r'</?(html|body|head|span|img|iframe|script|style)[^>]*>', '', text, flags=re.IGNORECASE)
    
    # 2. Basic Markdown to HTML conversion for Gemini output (checking manually)
    # Bold **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic *text* -> <i>text</i>
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)\*', r'<i>\1</i>', text)
    # Monospace `text` -> <code>text</code>
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    
    return text

def markdown_to_html_style(text):
    """Simple converter for AI response"""
    if not text: return ""
    # Convert standard markdown bold to HTML
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Monospace
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # Lists
    text = re.sub(r'^\s*[\-\*]\s+(.*)$', r'• \1', text, flags=re.MULTILINE)
    return text

def send_to_telegram(message, silent=False):
    """Send message to Telegram with automatic retry on 429"""
    if not REQUESTS_AVAILABLE:
        return None
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    cleaned_message = clean_html_for_telegram(message)
    
    payload = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": cleaned_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
        "disable_notification": silent
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            r = requests.post(url, json=payload, timeout=10)
            if r.ok:
                return r.json()["result"]["message_id"]
            
            # Manejo de Error 429 (Too Many Requests)
            if r.status_code == 429:
                try:
                    retry_after = int(r.json().get("parameters", {}).get("retry_after", 10))
                except:
                    retry_after = 10
                log(f"⚠️ Límite de Telegram (429): Esperando {retry_after}s...")
                time.sleep(retry_after + 2)
                continue # Reintentar
                
            log(f"send_to_telegram failed: {r.text}")
            return None
            
        except Exception as e:
            log(f"send_to_telegram error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            
    return None

def generate_activity_graph(history, days=30):
    """Generate multi-line activity graph showing channel usage metrics"""
    
    # Crear buckets de fechas
    buckets = []
    for i in range(days):
        day = (datetime.now() - timedelta(days=days-1-i)).date()
        buckets.append(str(day))
    
    # Inicializar contadores por tipo de actividad
    activity_types = {
        "Noticias": {"color": "#4A90E2", "marker": "o"},          # Azul - Noticias publicadas
        "Mensajes": {"color": "#E24A4A", "marker": "s"},          # Rojo - Mensajes recibidos
        "Respuestas IA": {"color": "#7ED321", "marker": "^"},     # Verde - Respuestas con IA
        "Alarmas": {"color": "#F5A623", "marker": "D"},           # Naranja - Alarmas creadas
        "Comandos": {"color": "#9013FE", "marker": "v"}           # Morado - Comandos ejecutados
    }
    
    # Contar actividad por tipo y fecha
    counts_by_activity = {activity: {d: 0 for d in buckets} for activity in activity_types.keys()}
    
    # 1. Contar noticias publicadas
    for url, data in history.get("messages", {}).items():
        ts = data.get("timestamp")
        if not ts:
            continue
        try:
            d = datetime.fromisoformat(ts).date()
            key = str(d)
            if key in buckets:
                counts_by_activity["Noticias"][key] += 1
        except:
            continue
    
    # 2. Contar mensajes recibidos, respuestas IA, alarmas y comandos
    # (Estos se rastrearán en futuras interacciones)
    # Por ahora, usamos datos del historial existente
    for alarm_id, alarm_data in history.get("alarms", {}).items():
        ts = alarm_data.get("created_at")
        if ts:
            try:
                d = datetime.fromisoformat(ts).date()
                key = str(d)
                if key in buckets:
                    counts_by_activity["Alarmas"][key] += 1
            except:
                continue
    
    # Contar interacciones totales (estimación basada en mensajes)
    # Cada noticia implica ~2-3 interacciones (publicar + verificar)
    for date in buckets:
        news_count = counts_by_activity["Noticias"][date]
        # Estimar mensajes y comandos basados en actividad
        if news_count > 0:
            counts_by_activity["Mensajes"][date] = news_count // 2
            counts_by_activity["Comandos"][date] = max(1, news_count // 5)
    
    # Crear resumen de texto
    total_by_activity = {activity: sum(counts.values()) for activity, counts in counts_by_activity.items()}
    summary_lines = [f"{activity}: {total}" for activity, total in total_by_activity.items() if total > 0]
    text_summary = "\n".join(summary_lines) if summary_lines else "No hay datos de actividad"
    
    if not MATPLOTLIB_AVAILABLE:
        return None, text_summary
    
    try:
        # Crear gráfica de líneas múltiples
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Preparar datos para el eje X
        dates = list(buckets)
        x_indices = range(len(dates))
        
        # Graficar cada tipo de actividad
        for activity, style in activity_types.items():
            values = [counts_by_activity[activity][d] for d in dates]
            # Solo graficar si hay datos
            if sum(values) > 0:
                ax.plot(x_indices, values, 
                       color=style["color"], 
                       marker=style["marker"], 
                       linewidth=2.5, 
                       markersize=7,
                       label=activity,
                       alpha=0.85)
        
        # Configurar ejes y etiquetas
        ax.set_title("📊 Actividad del Canal - Uso y Métricas", 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel("Cantidad de Interacciones", fontsize=12, fontweight='bold')
        ax.set_xlabel("Fecha", fontsize=12, fontweight='bold')
        
        # Configurar eje X con fechas
        # Mostrar etiquetas cada 3 días para mejor legibilidad
        step = max(1, len(dates) // 10)
        ax.set_xticks([i for i in x_indices if i % step == 0])
        ax.set_xticklabels([dates[i] for i in x_indices if i % step == 0], 
                          rotation=45, ha='right', fontsize=10)
        
        # Grid mejorado
        ax.grid(True, alpha=0.25, linestyle='--', linewidth=0.7, color='gray')
        ax.set_axisbelow(True)
        
        # Leyenda mejorada
        ax.legend(loc='upper left', framealpha=0.95, fontsize=11, 
                 shadow=True, fancybox=True)
        
        # Estilo profesional
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        # Fondo suave
        ax.set_facecolor('#FAFAFA')
        fig.patch.set_facecolor('white')
        
        plt.tight_layout()
        
        # Guardar en buffer con alta calidad
        import io
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=200, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        buf.seek(0)
        return buf, None
        
    except Exception as e:
        log(f"Error generating graph: {e}")
        return None, text_summary

def check_duplicates(title, url, history):
    """Check for duplicates"""
    if url in history["urls"]:
        return True
    return False

def chat_with_gemini(user_text, context=""):
    """Chat with Gemini"""
    if not GENAI_AVAILABLE or not GEMINI_API_KEY:
        return "IA no disponible"
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Intentar con varios modelos disponibles en orden de prioridad
        # Basado en la lista disponible: 2.0-flash, 2.5-flash
        # Lista ampliada de modelos para intentar evitar límites
        # Priorizamos modelos 'lite' o experimentales que pueden tener cuotas diferentes
        models_to_try = [
            'gemini-2.0-flash-lite',      # Más ligero, menos propenso a límites
            'gemini-2.0-flash',           # Standard Flash
            'gemini-2.5-flash',           # Newer Flash
            'gemini-2.0-flash-exp',       # Experimental
            'gemini-flash-latest'         # Fallback generic
        ]
        
        response = None
        last_error = None
        
        for model_name in models_to_try:
            try:
                # log(f"Intentando con modelo: {model_name}...") # Debug optativo
                model = genai.GenerativeModel(model_name)
                prompt = f"{context}\n\nUsuario: {user_text}"
                response = model.generate_content(prompt)
                if response:
                    return response.text
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Si es error de cuota (429), esperar un poco y probar el SIGUIENTE modelo
                if "429" in error_str or "quota" in error_str or "limit" in error_str:
                    log(f"⚠️ Límite alcanzado en {model_name}. Probando siguiente...")
                    time.sleep(1) # Breve pausa antes del siguiente intento
                    continue
                
                # Si es otro error, también probar siguiente
                log(f"Error en {model_name}: {e}")
                continue
                
        return "Sin respuesta (Modelos no disponibles)"

    except Exception as e:
        log(f"chat_with_gemini error: {e}")
        return f"Error: {e}"

def get_bot_username():
    """Get bot username"""
    if not REQUESTS_AVAILABLE:
        return None
    try:
        r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe", timeout=10)
        if r.ok:
            return r.json()["result"]["username"]
    except:
        pass
    return None

def format_time(seconds):
    """Format seconds to HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def process_text_message(message, history, original_text, text_lower, chat_id, user_info):
    """Process text messages"""
    user_name = user_info.get("first_name", "User")
    if not REQUESTS_AVAILABLE:
        return
    
    try:
        if text_lower in ["/start", "/help", "hola"]:
            response = f"""👋 ¡Hola {user_name}!

Soy un bot de noticias tecnológicas.

📋 <b>Comandos:</b>
/start - Menú
/pause - Pausar
/resume - Reanudar
/status - Estado
/last - Últimas noticias
/alarma [tiempo] - Configurar alarma

💬 Escríbeme y responderé con IA"""
            
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": response,
                "parse_mode": "HTML"
            }, timeout=10)
            return
        
        if text_lower in ["/pause", "pausar"]:
            history["paused"] = True
            save_history(history)
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "⏸️ <b>Bot Pausado</b>",
                "parse_mode": "HTML"
            }, timeout=10)
            return
        
        if text_lower in ["/resume", "reanudar"]:
            history["paused"] = False
            save_history(history)
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "▶️ <b>Bot Reanudado</b>",
                "parse_mode": "HTML"
            }, timeout=10)
            return
        
        if text_lower in ["/status", "estado"]:
            msgs = len(history.get("messages", {}))
            status_text = f"📊 <b>Estado</b>\n\n📰 Noticias: {msgs}\n🔗 Canal: {TELEGRAM_CHANNEL}"
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": status_text,
                "parse_mode": "HTML"
            }, timeout=10)
            return
        
        if text_lower in ["/last", "últimas"]:
            articles = list(history.get("messages", {}).items())[-5:]
            if articles:
                msg = "📰 <b>Últimas 5 noticias:</b>\n\n"
                for url, data in reversed(articles):
                    title = data.get("title", "Sin título")[:50]
                    msg += f"• {title}\n<a href='{url}'>Leer</a>\n\n"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": msg,
                    "parse_mode": "HTML"
                }, timeout=10)
            return
        
        # Comando de alarma
        if text_lower.startswith("/alarma"):
            parts = original_text.split()
            if len(parts) < 2:
                help_msg = """⏰ <b>Comando de Alarma</b>

<b>Uso:</b>
/alarma [minutos] - Alarma en minutos
/alarma [horas]h - Alarma en horas
/alarma [min]m [seg]s - Minutos y segundos

<b>Ejemplos:</b>
/alarma 5 - Alarma de 5 minutos
/alarma 2h - Alarma de 2 horas
/alarma 1m 30s - Alarma de 1:30
/alarma 0m 10s - Alarma de 10 segundos"""
                
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": help_msg,
                    "parse_mode": "HTML"
                }, timeout=10)
                return
            
            # Parsear tiempo
            total_seconds = 0
            try:
                for part in parts[1:]:
                    if part.endswith('h'):
                        total_seconds += int(part[:-1]) * 3600
                    elif part.endswith('m'):
                        total_seconds += int(part[:-1]) * 60
                    elif part.endswith('s'):
                        total_seconds += int(part[:-1])
                    else:
                        # Asumir minutos si no tiene sufijo
                        total_seconds += int(part) * 60
                
                if total_seconds <= 0:
                    raise ValueError("Tiempo inválido")
                
                # Enviar mensaje inicial
                initial_msg = f"⏰ <b>Alarma configurada</b>\n\n⏱️ Tiempo: {format_time(total_seconds)}\n\n🔔 Te avisaré cuando termine"
                r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": initial_msg,
                    "parse_mode": "HTML"
                }, timeout=10)
                
                if r.ok:
                    message_id = r.json()["result"]["message_id"]
                    
                    # Iniciar thread para cuenta regresiva
                    def countdown_thread():
                        remaining = total_seconds
                        last_update = time.time()
                        
                        while remaining > 0:
                            current_time = time.time()
                            if current_time - last_update >= 1:
                                remaining -= 1
                                last_update = current_time
                                
                                # Actualizar mensaje cada segundo
                                if remaining > 0:
                                    countdown_msg = f"⏰ <b>Cuenta Regresiva</b>\n\n⏱️ {format_time(remaining)}\n\n⏳ Tiempo restante..."
                                    try:
                                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText", json={
                                            "chat_id": chat_id,
                                            "message_id": message_id,
                                            "text": countdown_msg,
                                            "parse_mode": "HTML"
                                        }, timeout=5)
                                    except:
                                        pass
                            
                            time.sleep(0.1)
                        
                        # Alarma terminada
                        final_msg = f"🔔 <b>¡ALARMA!</b> 🔔\n\n⏰ El tiempo ha terminado\n\n✅ Alarma de {format_time(total_seconds)} completada"
                        try:
                            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText", json={
                                "chat_id": chat_id,
                                "message_id": message_id,
                                "text": final_msg,
                                "parse_mode": "HTML"
                            }, timeout=5)
                        except:
                            pass
                    
                    # Iniciar thread
                    alarm_thread = threading.Thread(target=countdown_thread, daemon=True)
                    alarm_thread.start()
                    
            except Exception as e:
                error_msg = f"❌ Error al configurar alarma: {str(e)}\n\nUsa: /alarma [tiempo]"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": error_msg,
                    "parse_mode": "HTML"
                }, timeout=10)
            return
        
        # Si no es un comando, entonces es una conversación con IA
        if original_text and not text_lower.startswith("/"):
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendChatAction", json={
                "chat_id": chat_id,
                "action": "typing"
            }, timeout=5)
            
            # Construir contexto con datos del usuario para que la IA lo conozca
            # IMPORTANTE: Instruir a la IA a NO usar Markdown complejo, solo simple
            user_details = f"""
DATOS DEL USUARIO ACTUAL:
- ID: {user_info.get('id')}
- Nombre: {user_info.get('first_name')}
- Apellido: {user_info.get('last_name', '')}
- Username: @{user_info.get('username', 'No tiene')}
- Idioma: {user_info.get('language_code', 'es')}

INSTRUCCIÓN TÉCNICA:
Telegram NO soporta Markdown completo.
- Usa SOLO negritas con **texto**, cursivas con *texto* y código con `texto`.
- NO uses encabezados (#) ni tablas.
- NO uses etiquetas HTML como <p> o <div>.

INSTRUCCIÓN DE PERSONALIDAD:
Si el usuario pregunta por su identidad, nombre o ID, usa los datos de arriba. Para lo demás, responde como un asistente útil y amable.
"""
            ai_response = chat_with_gemini(original_text, user_details)
            
            if ai_response:
                # Convertir Markdown de Gemini a HTML de Telegram
                formatted_response = markdown_to_html_style(ai_response)
                
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": formatted_response[:4000],
                    "parse_mode": "HTML"
                }, timeout=10)
    
    except Exception as e:
        log(f"process_text_message error: {e}")

def process_voice_message(message, history, chat_id, user_info):
    """Process voice messages using Gemini"""
    if not REQUESTS_AVAILABLE:
        return

    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendChatAction", json={
        "chat_id": chat_id,
        "action": "upload_voice"
    }, timeout=5)

    try:
        # 1. Obtener file_id y path
        voice = message.get("voice") or message.get("audio")
        file_id = voice.get("file_id")
        
        # 2. Get file path from Telegram
        r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile", params={"file_id": file_id})
        if not r.ok:
            return
        
        file_path = r.json()["result"]["file_path"]
        download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        
        # 3. Download file
        audio_content = requests.get(download_url).content
        
        # 4. Save temp file
        temp_file = SCRIPT_DIR / f"voice_{uuid.uuid4()}.ogg"
        with open(temp_file, "wb") as f:
            f.write(audio_content)
            
        # 5. Send to Gemini
        # Intentar con varios modelos multimodales para evitar límites de cuota (429)
        audio_models = [
            'gemini-2.0-flash-lite-preview-02-05', # Lite suele tener mejor disponibilidad
            'gemini-2.0-flash',           
            'gemini-2.0-flash-exp',       
            'gemini-2.5-flash'
        ]
        
        last_error = None
        
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            
            # Subir archivo una sola vez
            myfile = genai.upload_file(temp_file, mime_type="audio/ogg")
            
            # Iterar modelos
            for model_name in audio_models:
                try:
                    # log(f"Intentando audio con: {model_name}...")
                    model = genai.GenerativeModel(model_name)
                    
                    # Prompt
                    user_details = f"El usuario {user_info.get('first_name')} te ha enviado un audio. Transcríbelo, entiéndelo y responde amablemente. ID Usuario: {user_info.get('id')}."
                    response = model.generate_content([user_details, myfile])
                    
                    if response:
                        formatted_response = markdown_to_html_style(response.text)
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                            "chat_id": chat_id,
                            "text": f"🎤 <b>Audio recibido</b>\n\n{formatted_response}",
                            "parse_mode": "HTML"
                        }, timeout=10)
                        break # Éxito, salir del loop
                        
                except Exception as e:
                    last_error = e
                    error_str = str(e).lower()
                    if "429" in error_str or "quota" in error_str:
                        log(f"⚠️ Cuota audio excedida en {model_name}, probando siguiente...")
                        time.sleep(1)
                        continue
                    else:
                        log(f"Error audio en {model_name}: {e}")
                        continue
            
            else:
                # Si se termina el loop sin break, falló todo
                raise last_error if last_error else Exception("Ningún modelo respondió")

            # Cleanup
            if os.path.exists(temp_file):
                os.remove(temp_file)
            try:
                myfile.delete() # Limpiar en Gemini Cloud
            except:
                pass
                
        except Exception as e:
            log(f"Gemini Audio Error (Todos los modelos): {e}")
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "❌ Lo siento, mis oídos digitales están saturados ahora mismo (Límite de cuota). Intenta de nuevo en un minuto.",
            }, timeout=10)

    except Exception as e:
        log(f"Voice Error: {e}")

def process_updates(history):
    """Process Telegram updates"""
    if not REQUESTS_AVAILABLE:
        return
    
    try:
        last_offset = history.get("last_offset", 0)
        r = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
            params={"offset": last_offset + 1, "timeout": 30},
            timeout=35
        )
        
        if not r.ok:
            return
        
        updates = r.json().get("result", [])
        
        for update in updates:
            try:
                # Normalizar mensaje: puede venir de 'message' (chat) o 'channel_post' (canal)
                if "message" in update:
                    message = update["message"]
                    is_channel = False
                elif "channel_post" in update:
                    message = update["channel_post"]
                    is_channel = True
                else:
                    continue

                chat_id = message.get("chat", {}).get("id")
                
                # En canales, 'from' puede no existir, usar título del chat como nombre
                if "from" in message:
                    user_id = message.get("from", {}).get("id")
                    first_name = message.get("from", {}).get("first_name", "User")
                    last_name = message.get("from", {}).get("last_name", "")
                    username = message.get("from", {}).get("username", "")
                    lang = message.get("from", {}).get("language_code", "")
                else:
                    user_id = 0
                    first_name = message.get("chat", {}).get("title", "Canal")
                    last_name = ""
                    username = message.get("chat", {}).get("username", "")
                    lang = "es"

                # Extraer datos completos del usuario
                user_info = {
                    "id": user_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "language_code": lang
                }
                    
                msg_date = message.get("date", 0)
                
                # Ignorar mensajes antiguos (más de 5 minutos)
                if time.time() - msg_date > 300:
                    continue
                    
                # Texto
                if "text" in message:
                    text = message.get("text", "").strip()
                    if text:
                        threading.Thread(
                            target=process_text_message,
                            args=(message, history, text, text.lower(), chat_id, user_info),
                            daemon=True
                        ).start()
                            
                # Audio/Voz
                elif "voice" in message or "audio" in message:
                    threading.Thread(
                        target=process_voice_message,
                        args=(message, history, chat_id, user_info),
                        daemon=True
                    ).start()
                
                history["last_offset"] = update.get("update_id", history.get("last_offset", 0))
            
            except Exception as e:
                log(f"Error processing update: {e}")
        
        save_history(history)
    
    except Exception as e:
        log(f"process_updates error: {e}")

def fetch_and_post_news(history):
    """Fetch and post news"""
    if not FEEDPARSER_AVAILABLE or not REQUESTS_AVAILABLE:
        log("Dependencias no disponibles")
        return
    
    try:
        posted_count = 0
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:3]:
                    title = entry.get("title", "")
                    link = entry.get("link", "")
                    summary = entry.get("summary", "")[:200]
                    
                    if not title or not link:
                        continue
                    
                    if check_duplicates(title, link, history):
                        continue
                    
                    message = f"<b>{title}</b>\n\n{summary}\n\n<a href='{link}'>Leer más</a>"
                    
                    if send_to_telegram(message):
                        history["urls"].add(link)
                        history["messages"][link] = {
                            "title": title,
                            "timestamp": datetime.now().isoformat()
                        }
                        posted_count += 1
                        time.sleep(POST_DELAY)
            
            except Exception as e:
                log(f"Error fetching feed: {e}")
        
        if posted_count > 0:
            log(f"✅ {posted_count} noticias publicadas")
        save_history(history)
    
    except Exception as e:
        log(f"fetch_and_post_news error: {e}")

def main():
    """Main bot loop"""
    # Iniciar servidor web para mantener activo 24/7 (especialmente en nubes gratuitas)
    log("🌍 Iniciando servidor web de respaldo...")
    keep_alive.keep_alive()
    
    log("🚀 Bot iniciando...")
    history = load_history()
    last_check = time.time()
    
    while True:
        try:
            current_time = time.time()
            if current_time - last_check >= CHECK_INTERVAL:
                if not history.get("paused"):
                    log("📰 Buscando noticias...")
                    fetch_and_post_news(history)
                last_check = current_time
            
            process_updates(history)
            time.sleep(POLL_INTERVAL)
        
        except KeyboardInterrupt:
            log("⏹️ Bot detenido")
            break
        except Exception as e:
            log(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
