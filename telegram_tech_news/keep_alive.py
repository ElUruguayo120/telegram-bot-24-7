import os
from pathlib import Path
from flask import Flask
from threading import Thread

app = Flask('')

# Ruta al archivo de logs
LOG_FILE = Path(__file__).parent / "bot.log"

@app.route('/')
def home():
    try:
        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                # Leer últimas 50 líneas
                lines = f.readlines()[-50:]
                log_content = "".join(lines)
        else:
            log_content = "Esperando logs..."
    except Exception as e:
        log_content = f"Error leyendo logs: {e}"

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="5"> <!-- Auto-refresco cada 5s -->
        <title>🤖 Bot Monitor 24/7</title>
        <style>
            body {{
                font-family: 'Courier New', monospace;
                background-color: #0d1117;
                color: #c9d1d9;
                padding: 20px;
                margin: 0;
            }}
            .header {{
                text-align: center;
                padding: 20px;
                border-bottom: 1px solid #30363d;
                margin-bottom: 20px;
            }}
            .status {{
                color: #2ea043;
                font-weight: bold;
                font-size: 1.2em;
            }}
            .logs-container {{
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 15px;
                overflow-x: auto;
                white-space: pre-wrap;
                font-size: 14px;
                height: 70vh;
                overflow-y: auto;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }}
            .log-line {{
                margin-bottom: 4px;
                border-bottom: 1px solid #21262d;
                padding-bottom: 2px;
            }}
            /* Scrollbar bonita */
            ::-webkit-scrollbar {{ width: 10px; }}
            ::-webkit-scrollbar-track {{ background: #0d1117; }}
            ::-webkit-scrollbar-thumb {{ background: #30363d; border-radius: 5px; }}
            ::-webkit-scrollbar-thumb:hover {{ background: #58a6ff; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 Telegram Bot Monitor</h1>
            <p class="status">● OPERATIVO Y ESCUCHANDO</p>
            <p style="font-size: 0.9em; color: #8b949e;">iPad Server Mode Active</p>
        </div>
        
        <div class="logs-container" id="logs">
            {log_content}
        </div>

        <script>
            // Auto-scroll al fondo
            var logs = document.getElementById("logs");
            logs.scrollTop = logs.scrollHeight;
        </script>
    </body>
    </html>
    """
    return html

def run():
    # Desactivar logs de Flask para no ensuciar
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()
