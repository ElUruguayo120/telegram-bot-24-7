#!/usr/bin/env python3
"""
Quick test to send a message to the channel
"""

import requests

TELEGRAM_BOT_TOKEN = "6631440619:AAHaQrfN0pOZ2RiGP8rvrjprOft45Yl6aPQ"
TELEGRAM_CHANNEL = "@Portal_tech2"

print("🧪 Intentando enviar mensaje de prueba...\n")

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

test_message = """🎉 <b>¡Bot Activado!</b>

Tu bot de noticias tecnológicas está funcionando correctamente.

Pronto comenzarás a recibir las últimas noticias sobre:
📱 Móviles y smartphones
💻 Ordenadores y laptops
🎮 Consolas y gaming
🍎 Apple y competencia
⚡ Tecnología en general

🔗 <a href='https://telegram.org'>Powered by Telegram</a>"""

payload = {
    "chat_id": TELEGRAM_CHANNEL,
    "text": test_message,
    "parse_mode": "HTML",
    "disable_web_page_preview": False
}

try:
    response = requests.post(url, json=payload, timeout=10)
    data = response.json()
    
    print(f"Status Code: {response.status_code}")
    print(f"Response OK: {data.get('ok')}\n")
    
    if data.get("ok"):
        print("✅ ¡ÉXITO! Mensaje enviado al canal")
        print(f"Message ID: {data.get('result', {}).get('message_id')}")
        print(f"\n🎉 El bot está funcionando perfectamente!")
        print(f"\nAhora puedes:")
        print(f"1. Ejecutar el bot: python3 news_bot.py")
        print(f"2. O instalarlo en PythonAnywhere como Scheduled Task")
    else:
        print("❌ Error al enviar mensaje")
        print(f"Descripción: {data.get('description')}")
        print(f"Error Code: {data.get('error_code')}")
        print(f"\nRespuesta completa: {data}")
        
        if "not found" in str(data.get('description', '')).lower():
            print("\n⚠️ El canal no fue encontrado. Verifica:")
            print(f"   - Que el canal sea público")
            print(f"   - Que el username sea exactamente '@Portal_tech2'")
        elif "forbidden" in str(data.get('description', '')).lower() or "chat not found" in str(data.get('description', '')).lower():
            print("\n⚠️ El bot no tiene permisos. Asegúrate de:")
            print(f"   1. Añadir el bot como administrador del canal")
            print(f"   2. Darle permiso de 'Publicar mensajes'")
            
except Exception as e:
    print(f"❌ Error de conexión: {e}")