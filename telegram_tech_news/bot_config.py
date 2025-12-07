
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
HISTORY_FILE = BASE_DIR / "posted_articles.json"
LOG_FILE = BASE_DIR / "bot.log"
ENV_FILE = BASE_DIR / ".env"

# Load environment variables
if ENV_FILE.exists():
    with open(ENV_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_CHANNEL = "@Portal_tech2"
ADMIN_ID = 701604375

# RSS Feeds
RSS_FEEDS = [
    "https://www.xataka.com/index.xml",
    "https://www.genbeta.com/index.xml",
    "https://www.applesfera.com/index.xml",
]

# Settings
POST_DELAY = 1
