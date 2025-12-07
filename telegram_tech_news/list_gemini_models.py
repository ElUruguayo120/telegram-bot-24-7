#!/usr/bin/env python3
"""
Script para listar modelos disponibles de Gemini
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

try:
    import google.generativeai as genai
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    print("📋 Listando modelos disponibles de Gemini:\n")
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Descripción: {model.display_name}")
            print()
    
except Exception as e:
    print(f"❌ Error: {e}")
