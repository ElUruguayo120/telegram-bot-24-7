#!/bin/bash
# Wrapper script to run the Telegram Tech News Bot with environment variables

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Load environment variables from common shell config files
if [ -f ~/.zshrc ]; then
    source ~/.zshrc
fi

if [ -f ~/.bash_profile ]; then
    source ~/.bash_profile
fi

if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

if [ -f ~/.profile ]; then
    source ~/.profile
fi

# Also try to load from a .env file in the script directory
if [ -f "$SCRIPT_DIR/.env" ]; then
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        # Remove quotes if present
        value=$(echo "$value" | sed 's/^"//;s/"$//')
        export "$key=$value"
    done < "$SCRIPT_DIR/.env"
fi

# Also try to load from ~/prueba/.env (alternative location)
if [ -f ~/prueba/.env ]; then
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        value=$(echo "$value" | sed 's/^"//;s/"$//')
        export "$key=$value"
    done < ~/prueba/.env
fi

# Get Python3 path
PYTHON3=$(which python3)

# Check if variables are set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "ERROR: TELEGRAM_BOT_TOKEN not set!" >> "$SCRIPT_DIR/bot.log"
    exit 1
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "ERROR: GEMINI_API_KEY not set!" >> "$SCRIPT_DIR/bot.log"
    exit 1
fi

# Export variables explicitly
export TELEGRAM_BOT_TOKEN
export GEMINI_API_KEY

# Run the bot
exec "$PYTHON3" "$SCRIPT_DIR/news_bot.py"

