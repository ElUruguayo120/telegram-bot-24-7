#!/usr/bin/env python3
"""
🔄 Auto-Sync to PythonAnywhere
Sincroniza automáticamente los archivos modificados con PythonAnywhere usando su API
"""

import os
import sys
import requests
import base64
from pathlib import Path

# Configuración
PYTHONANYWHERE_USER = "Eluruguayo1900"
PYTHONANYWHERE_API_TOKEN = None  # Se configurará más adelante

# Archivos a sincronizar
FILES_TO_SYNC = [
    "news_bot.py",
    "run_task.py",
    "requirements.txt",
    ".env"
]

def print_header():
    """Imprime el encabezado del script"""
    print("=" * 50)
    print("🔄 Auto-Sync to PythonAnywhere")
    print("=" * 50)
    print()

def get_api_token():
    """Obtiene el API token de PythonAnywhere"""
    token_file = Path.home() / ".pythonanywhere_token"
    
    if token_file.exists():
        with open(token_file, 'r') as f:
            return f.read().strip()
    
    print("⚠️  No se encontró el API token de PythonAnywhere")
    print()
    print("Para obtener tu API token:")
    print(f"1. Ve a: https://www.pythonanywhere.com/user/{PYTHONANYWHERE_USER}/account/#api_token")
    print("2. Copia tu API token")
    print("3. Pégalo aquí:")
    print()
    
    token = input("API Token: ").strip()
    
    # Guardar token para futuras ejecuciones
    save = input("¿Guardar token para futuras sincronizaciones? (s/n): ").lower()
    if save == 's':
        with open(token_file, 'w') as f:
            f.write(token)
        print(f"✓ Token guardado en: {token_file}")
    
    return token

def upload_file_to_pythonanywhere(filepath, token):
    """Sube un archivo a PythonAnywhere usando la API"""
    filename = os.path.basename(filepath)
    remote_path = f"/home/{PYTHONANYWHERE_USER}/telegram_tech_news/{filename}"
    
    print(f"📤 Subiendo: {filename}...", end=" ")
    
    # Leer el contenido del archivo
    with open(filepath, 'rb') as f:
        content = f.read()
    
    # URL de la API
    url = f"https://www.pythonanywhere.com/api/v0/user/{PYTHONANYWHERE_USER}/files/path{remote_path}"
    
    # Headers
    headers = {
        'Authorization': f'Token {token}'
    }
    
    # Subir archivo
    response = requests.post(
        url,
        headers=headers,
        files={'content': content}
    )
    
    if response.status_code in [200, 201]:
        print("✅")
        return True
    else:
        print(f"❌ Error {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return False

def sync_files():
    """Sincroniza todos los archivos con PythonAnywhere"""
    print_header()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("news_bot.py"):
        print("❌ Error: No estás en el directorio telegram_tech_news")
        print("   Por favor, ejecuta este script desde el directorio telegram_tech_news")
        sys.exit(1)
    
    # Obtener API token
    token = get_api_token()
    
    if not token:
        print("❌ Error: No se proporcionó un API token")
        sys.exit(1)
    
    print()
    print("🔄 Sincronizando archivos...")
    print()
    
    # Subir cada archivo
    success_count = 0
    for filename in FILES_TO_SYNC:
        if os.path.exists(filename):
            if upload_file_to_pythonanywhere(filename, token):
                success_count += 1
        else:
            print(f"⚠️  Archivo no encontrado: {filename}")
    
    print()
    print("=" * 50)
    print(f"✅ Sincronización completada: {success_count}/{len(FILES_TO_SYNC)} archivos")
    print("=" * 50)
    print()
    print("💡 Tip: Los cambios se aplicarán en la próxima ejecución programada")
    print(f"   Próxima ejecución: XX:00 UTC (cada hora en punto)")
    print()

if __name__ == "__main__":
    try:
        sync_files()
    except KeyboardInterrupt:
        print("\n\n⚠️  Sincronización cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
