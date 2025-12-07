#!/usr/bin/env python3
"""
Test script for Telegram Tech News Bot
This will verify your configuration without spamming your channel
"""

import feedparser
import requests
import json
from datetime import datetime

# Import configuration from news_bot
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Configuration
TELEGRAM_BOT_TOKEN = "6631440619:AAHaQrfN0pOZ2RiGP8rvrjprOft45Yl6aPQ"
TELEGRAM_CHANNEL = "@Portal_tech2"

def test_bot_token():
    """Test if the bot token is valid"""
    print("=" * 60)
    print("TEST 1: Verificando Bot Token")
    print("=" * 60)
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            bot_info = data.get("result", {})
            print("✅ Bot Token VÁLIDO")
            print(f"   Nombre del bot: {bot_info.get('first_name')}")
            print(f"   Username: @{bot_info.get('username')}")
            print(f"   Bot ID: {bot_info.get('id')}")
            return True
        else:
            print("❌ Bot Token INVÁLIDO")
            print(f"   Error: {data}")
            return False
    except Exception as e:
        print(f"❌ Error al verificar el token: {e}")
        return False

def test_channel_access():
    """Test if the bot can access the channel"""
    print("\n" + "=" * 60)
    print("TEST 2: Verificando Acceso al Canal")
    print("=" * 60)
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChat"
    
    try:
        response = requests.get(url, params={"chat_id": TELEGRAM_CHANNEL}, timeout=10)
        data = response.json()
        
        if data.get("ok"):
            chat_info = data.get("result", {})
            print("✅ Canal ENCONTRADO")
            print(f"   Nombre: {chat_info.get('title')}")
            print(f"   Tipo: {chat_info.get('type')}")
            print(f"   Username: @{chat_info.get('username', 'N/A')}")
            
            # Check if bot is admin
            admin_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember"
            bot_me = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe").json()
            bot_id = bot_me.get("result", {}).get("id")
            
            admin_response = requests.get(admin_url, params={
                "chat_id": TELEGRAM_CHANNEL,
                "user_id": bot_id
            }, timeout=10)
            
            admin_data = admin_response.json()
            if admin_data.get("ok"):
                status = admin_data.get("result", {}).get("status")
                if status in ["administrator", "creator"]:
                    print(f"✅ El bot ES administrador del canal (status: {status})")
                    return True
                else:
                    print(f"⚠️  El bot NO es administrador (status: {status})")
                    print("   Necesitas añadir el bot como administrador del canal")
                    return False
        else:
            print("❌ No se puede acceder al canal")
            print(f"   Error: {data.get('description')}")
            print("\n   Posibles causas:")
            print("   - El nombre del canal es incorrecto")
            print("   - El canal no es público")
            print("   - El bot no ha sido añadido al canal")
            return False
    except Exception as e:
        print(f"❌ Error al verificar el canal: {e}")
        return False

def test_rss_feeds():
    """Test RSS feed parsing"""
    print("\n" + "=" * 60)
    print("TEST 3: Probando Feeds RSS")
    print("=" * 60)
    
    test_feeds = [
        "https://www.xataka.com/index.xml",
        "https://www.theverge.com/rss/index.xml",
    ]
    
    articles_found = []
    
    for feed_url in test_feeds:
        try:
            print(f"\n📡 Obteniendo: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            if feed.entries:
                print(f"   ✅ {len(feed.entries)} artículos encontrados")
                
                # Show first article
                if feed.entries:
                    entry = feed.entries[0]
                    print(f"\n   Ejemplo de artículo:")
                    print(f"   📰 {entry.get('title', 'Sin título')[:60]}...")
                    print(f"   🔗 {entry.get('link', 'N/A')[:60]}...")
                    articles_found.append(entry)
            else:
                print(f"   ⚠️  No se encontraron artículos")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return articles_found

def test_send_message(dry_run=True):
    """Test sending a message to Telegram"""
    print("\n" + "=" * 60)
    print("TEST 4: Prueba de Envío de Mensaje")
    print("=" * 60)
    
    test_message = """🧪 <b>MENSAJE DE PRUEBA</b>

Este es un mensaje de prueba del bot de noticias tecnológicas.

Si ves este mensaje, ¡el bot está funcionando correctamente! 🎉

🔗 <a href='https://telegram.org'>Telegram</a>"""
    
    if dry_run:
        print("\n📋 MODO DRY RUN - No se enviará el mensaje")
        print("\nMensaje que se enviaría:")
        print("-" * 60)
        print(test_message.replace("<b>", "").replace("</b>", "").replace("<a href='https://telegram.org'>", "").replace("</a>", ""))
        print("-" * 60)
        
        response = input("\n¿Quieres enviar este mensaje de prueba al canal? (s/n): ")
        if response.lower() != 's':
            print("❌ Prueba cancelada")
            return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": test_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            print("✅ Mensaje enviado EXITOSAMENTE al canal!")
            print(f"   Message ID: {data.get('result', {}).get('message_id')}")
            return True
        else:
            print("❌ Error al enviar mensaje")
            print(f"   Error: {data}")
            return False
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
        return False

def main():
    """Run all tests"""
    print("\n🤖 TELEGRAM TECH NEWS BOT - SUITE DE PRUEBAS")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        "bot_token": False,
        "channel_access": False,
        "rss_feeds": False,
        "send_message": False
    }
    
    # Test 1: Bot Token
    results["bot_token"] = test_bot_token()
    
    if not results["bot_token"]:
        print("\n⚠️  No se puede continuar sin un token válido")
        return
    
    # Test 2: Channel Access
    results["channel_access"] = test_channel_access()
    
    # Test 3: RSS Feeds
    articles = test_rss_feeds()
    results["rss_feeds"] = len(articles) > 0
    
    # Test 4: Send Message (optional)
    if results["bot_token"] and results["channel_access"]:
        results["send_message"] = test_send_message(dry_run=True)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    all_passed = all([results["bot_token"], results["channel_access"], results["rss_feeds"]])
    
    if all_passed:
        print("\n🎉 ¡Todas las pruebas principales pasaron!")
        print("\n📝 Próximos pasos:")
        print("   1. El bot está listo para funcionar")
        print("   2. Ejecuta: python3 news_bot.py")
        print("   3. O instala como Scheduled Task en PythonAnywhere")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()