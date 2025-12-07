
#!/usr/bin/env python3
"""
RSS Job for PythonAnywhere Scheduled Task
Runs once, posts news, and exits.
"""
import time
import feedparser
from datetime import datetime
from .bot_config import RSS_FEEDS, POST_DELAY
from .bot_utils import (
    load_history, save_history, send_to_telegram, log, 
    clean_html_for_telegram
)

def check_duplicates(title, url, history):
    if url in history["urls"]:
        return True
    return False

def fetch_and_post_news():
    log("📰 RSS Job: Iniciando búsqueda de noticias...")
    history = load_history()
    
    if history.get("paused"):
        log("⏸️ Bot pausado. Saltando RSS.")
        return

    posted_count = 0
    
    for feed_url in RSS_FEEDS:
        try:
            log(f"📡 Leyendo: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            # Solo procesar las 3 más nuevas para evitar spam
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
                else:
                    log("❌ Error enviando mensaje a Telegram")
        
        except Exception as e:
            log(f"❌ Error procesando feed {feed_url}: {e}")
            
    if posted_count > 0:
        log(f"✅ {posted_count} noticias publicadas")
        save_history(history)
    else:
        log("✅ No hay noticias nuevas")

if __name__ == "__main__":
    fetch_and_post_news()
