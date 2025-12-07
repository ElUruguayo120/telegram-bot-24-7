#!/usr/bin/env python3
"""
Script para probar la integración con Gemini AI
"""
import os
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

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def test_gemini():
    """Prueba la conexión con Gemini AI"""
    print("🧪 Probando Gemini AI...")
    print(f"API Key (primeros 10 chars): {GEMINI_API_KEY[:10]}...")
    
    if not GEMINI_API_KEY:
        print("❌ No se encontró GEMINI_API_KEY en .env")
        return False
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("\n📤 Enviando pregunta de prueba a Gemini...")
        response = model.generate_content("Di 'Hola, estoy funcionando correctamente' en una frase corta")
        
        if response and response.text:
            print("\n✅ Gemini AI funcionando correctamente!")
            print(f"📝 Respuesta: {response.text}")
            return True
        else:
            print("\n❌ Gemini no devolvió respuesta")
            return False
    
    except Exception as e:
        print(f"\n❌ Error al conectar con Gemini: {e}")
        return False

if __name__ == "__main__":
    test_gemini()
