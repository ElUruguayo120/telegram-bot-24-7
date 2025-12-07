#!/usr/bin/env python3
"""
🌐 Browser Auto-Sync to PythonAnywhere
Sincroniza archivos automáticamente usando el navegador web
Este script es útil cuando no tienes acceso a la API
"""

import os
import sys
import time
import zipfile
from pathlib import Path

# Archivos a sincronizar
FILES_TO_SYNC = [
    "news_bot.py",
    "run_task.py",
    "requirements.txt",
    ".env"
]

def create_update_package():
    """Crea un paquete ZIP con los archivos actualizados"""
    print("=" * 50)
    print("🌐 Browser Auto-Sync to PythonAnywhere")
    print("=" * 50)
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("news_bot.py"):
        print("❌ Error: No estás en el directorio telegram_tech_news")
        sys.exit(1)
    
    print("📦 Creando paquete de actualización...")
    print()
    
    # Crear ZIP
    zip_path = "../pythonanywhere_update.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in FILES_TO_SYNC:
            if os.path.exists(filename):
                zipf.write(filename)
                print(f"  ✓ {filename}")
            else:
                print(f"  ⚠️  {filename} (no encontrado)")
    
    print()
    print("✅ Paquete creado exitosamente")
    print()
    
    return os.path.abspath(zip_path)

def print_instructions(zip_path):
    """Imprime las instrucciones para subir el archivo"""
    print("=" * 50)
    print("📋 PRÓXIMOS PASOS:")
    print("=" * 50)
    print()
    print("Voy a abrir PythonAnywhere en tu navegador.")
    print()
    print("Cuando se abra:")
    print()
    print("1. 📂 Ve a la sección 'Files'")
    print("2. 📤 Sube el archivo: pythonanywhere_update.zip")
    print("3. 💻 Abre una consola Bash")
    print("4. ⌨️  Ejecuta estos comandos:")
    print()
    print("   cd ~")
    print("   unzip -o pythonanywhere_update.zip -d telegram_tech_news/")
    print("   rm pythonanywhere_update.zip")
    print()
    print("=" * 50)
    print()
    
    input("Presiona ENTER para abrir PythonAnywhere en el navegador...")
    
    # Abrir PythonAnywhere en el navegador
    import webbrowser
    webbrowser.open("https://www.pythonanywhere.com/user/Eluruguayo1900/files/home/Eluruguayo1900")
    
    print()
    print("🌐 PythonAnywhere abierto en el navegador")
    print()
    print("💡 Tip: El archivo ZIP está en:")
    print(f"   {zip_path}")
    print()
    
    # Abrir el archivo en Finder
    os.system(f'open -R "{zip_path}"')
    
    print("📁 Finder abierto con el archivo ZIP")
    print()
    print("✅ ¡Listo! Ahora sube el archivo siguiendo las instrucciones")
    print()

if __name__ == "__main__":
    try:
        zip_path = create_update_package()
        print_instructions(zip_path)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
