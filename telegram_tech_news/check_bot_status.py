#!/usr/bin/env python3
"""
Script para verificar el estado del bot de Telegram
"""
import os
import requests
from pathlib import Path

# Cargar variables de entorno desde .env
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

def check_bot():
    """Verifica el estado del bot"""
    print("🔍 Verificando bot de Telegram...")
    print(f"Token (primeros 10 chars): {TELEGRAM_BOT_TOKEN[:10]}...")
    
    try:
        # Verificar bot
        r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe", timeout=10)
        
        if r.ok:
            data = r.json()
            result = data.get("result", {})
            print("\n✅ Bot conectado correctamente!")
            print(f"   • Nombre: {result.get('first_name')}")
            print(f"   • Username: @{result.get('username')}")
            print(f"   • ID: {result.get('id')}")
            print(f"   • Es bot: {result.get('is_bot')}")
            return True
        else:
            print(f"\n❌ Error al conectar con el bot:")
            print(f"   Código: {r.status_code}")
            print(f"   Respuesta: {r.text}")
            return False
    
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    check_bot()
