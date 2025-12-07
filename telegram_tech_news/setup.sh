#!/bin/bash
# Setup script for Telegram Tech News Bot

echo "🤖 Configurando Telegram Tech News Bot..."
echo "=========================================="

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cat > .env << EOF
TELEGRAM_BOT_TOKEN=tu_token_aqui
GEMINI_API_KEY=tu_api_key_aqui
EOF
    echo "⚠️  Por favor edita .env con tus credenciales"
fi

# Create necessary directories
mkdir -p logs

echo ""
echo "✅ ¡Configuración completada!"
echo ""
echo "Próximos pasos:"
echo "1. Edita el archivo .env con tus credenciales"
echo "2. Ejecuta: source .venv/bin/activate"
echo "3. Prueba: python3 test_bot.py"
echo "4. Ejecuta: python3 news_bot.py"
echo ""
