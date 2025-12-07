#!/usr/bin/env python3
"""
Test both channels to see which one has the bot
"""

import requests

TELEGRAM_BOT_TOKEN = "6631440619:AAHaQrfN0pOZ2RiGP8rvrjprOft45Yl6aPQ"

channels = ["@Portal_tech2", "@portaltech", "@portal"]

print("🔍 Probando canales...")
print("="*60)
print()

found_channel = None

for channel in channels:
    print(f"Probando: {channel}")
    
    # Get channel info
    chat_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChat"
    
    try:
        chat_response = requests.get(chat_url, params={"chat_id": channel}, timeout=10).json()
        
        if chat_response.get('ok'):
            chat_info = chat_response.get('result', {})
            print(f"   ✅ Canal encontrado: {chat_info.get('title')}")
            print(f"   ID: {chat_info.get('id')}")
            print(f"   Tipo: {chat_info.get('type')}")
            
            # Check if bot is admin
            bot_me_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
            bot_me = requests.get(bot_me_url, timeout=10).json()
            bot_id = bot_me.get("result", {}).get("id")
            
            member_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember"
            member_response = requests.get(member_url, params={
                "chat_id": channel,
                "user_id": bot_id
            }, timeout=10).json()
            
            if member_response.get('ok'):
                status = member_response.get('result', {}).get('status')
                if status in ["administrator", "creator"]:
                    print(f"   ✅ Bot es administrador")
                    found_channel = channel
                    
                    # Try to send message
                    send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                    
                    test_message = """🎉 <b>¡Bot de Noticias Tecnológicas Activado!</b>

¡Bienvenido! Tu canal ahora tiene un bot automático que publicará las últimas noticias de tecnología.

📰 <b>Fuentes monitoreadas:</b>
• Xataka, Genbeta, Applesfera
• The Verge, Engadget, TechCrunch

🔄 <b>Frecuencia:</b> Cada hora

📱 <b>Temas cubiertos:</b>
• 📱 Móviles y smartphones
• 💻 Ordenadores y laptops
• 🎮 Consolas y gaming
• 🍎 Apple y competencia
• ⚡ Tecnología en general

¡Tu canal está a punto de revivir! 🚀"""
                    
                    send_response = requests.post(send_url, json={
                        "chat_id": channel,
                        "text": test_message,
                        "parse_mode": "HTML"
                    }, timeout=10).json()
                    
                    if send_response.get('ok'):
                        print(f"   ✅ ¡ÉXITO! Mensaje enviado")
                    else:
                        print(f"   ⚠️  Error al enviar: {send_response.get('description')}")
                    
                    print()
                else:
                    print(f"   ⚠️  Bot NO es administrador (status: {status})")
            else:
                print(f"   ⚠️  Bot no está en el canal")
        else:
            error = chat_response.get('description', 'Error desconocido')
            print(f"   ❌ No encontrado: {error}")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()

print("="*60)
if found_channel:
    print(f"🎊 ¡CANAL CONFIGURADO: {found_channel}!")
    print("="*60)
    print()
    print(f"✅ Bot configurado en: {found_channel}")
    print()
    print("🚀 El bot está listo para funcionar!")
    print()
    print("Próximos pasos:")
    print()
    print("1️⃣  Ejecutar el bot manualmente:")
    print("   export TELEGRAM_BOT_TOKEN='6631440619:AAHaQrfN0pOZ2RiGP8rvrjprOft45Yl6aPQ'")
    print("   export GEMINI_API_KEY='tu_api_key'")
    print("   python3 news_bot.py")
    print()
    print("2️⃣  O instalar en PythonAnywhere como Scheduled Task:")
    print("   https://www.pythonanywhere.com/user/Eluruguayo1900/consoles/")
    print()
else:
    print("⚠️  El bot NO es administrador en ninguno de los canales")
    print("="*60)
    print()
    print("Por favor:")
    print("1. Abre Telegram")
    print("2. Ve a tu canal")
    print("3. Toca en el nombre del canal → Miembros")
    print("4. Añade @Marceloadmin_bot (o tu bot username)")
    print("5. Dale permisos de administrador:")
    print("   ✅ Publicar mensajes")
    print("   ✅ Editar mensajes")
    print("   ✅ Eliminar mensajes")
    print()