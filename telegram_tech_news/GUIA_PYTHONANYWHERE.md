# 🐍 Guía Completa: Desplegar en PythonAnywhere (GRATIS)

## ⚠️ Importante sobre PythonAnywhere

**Limitación del plan gratis:**
- ❌ No puede ejecutar procesos continuos 24/7
- ✅ Puede ejecutar tareas programadas cada hora (perfecto para tu bot)
- ✅ Tu bot seguirá funcionando incluso con tu Mac apagado

El bot se ejecutará **cada hora** automáticamente, que es perfecto porque ya tienes `CHECK_INTERVAL = 3600` (1 hora).

---

## 📋 Paso 1: Crear cuenta en PythonAnywhere

1. Ve a: https://www.pythonanywhere.com
2. Click en "Sign up for free"
3. Elige un nombre de usuario (ej: `marcelotech`)
4. Completa el registro (NO necesitas tarjeta de crédito)

---

## 📂 Paso 2: Subir tu código

### Opción A: Desde la interfaz web

1. **Accede al Dashboard**
   - Después de registrarte, verás el dashboard

2. **Crea una carpeta para tu bot**
   - Click en "Files" (menú superior)
   - Click en el ícono de carpeta para crear nueva carpeta
   - Nombre: `telegram_bot`

3. **Sube los archivos necesarios**
   - Entra a la carpeta `telegram_bot`
   - Click en "Upload a file"
   - Sube estos archivos:
     - `news_bot.py`
     - `requirements.txt`
     - `posted_articles.json` (si ya tienes historial)

### Opción B: Desde terminal (recomendado)

1. **Abre una consola Bash**
   - En el dashboard, click en "Consoles" → "New console" → "Bash"

2. **Crea la carpeta y descarga/copia los archivos**
   ```bash
   mkdir -p ~/telegram_bot
   cd ~/telegram_bot
   ```

3. **Crea los archivos directamente** (copia y pega el contenido)
   - Usa `nano` o el editor web para crear `news_bot.py` y `requirements.txt`

---

## 🔧 Paso 3: Instalar dependencias

En la consola Bash:

```bash
cd ~/telegram_bot
pip3.9 install --user feedparser requests google-generativeai beautifulsoup4
```

**Nota:** PythonAnywhere usa Python 3.9 por defecto, por eso usamos `pip3.9`

---

## ⚙️ Paso 4: Configurar variables de entorno

### Opción 1: Crear archivo .env (Recomendado)

1. En "Files", dentro de `telegram_bot`, crea un archivo llamado `.env`
2. Contenido:
   ```
   TELEGRAM_BOT_TOKEN=6665925860:AAHa-Eu8xKhece83HaKEsHTB8x8CGF61Czk
   GEMINI_API_KEY=AIzaSyAYgke20w4fNeZL_zK3wm8r19NgbIat6s0
   ```

### Opción 2: Modificar news_bot.py temporalmente

Como fallback, puedes modificar temporalmente las líneas 28 y 30 en `news_bot.py`:
```python
TELEGRAM_BOT_TOKEN = "6665925860:AAHa-Eu8xKhece83HaKEsHTB8x8CGF61Czk"
GEMINI_API_KEY = "AIzaSyAYgke20w4fNeZL_zK3wm8r19NgbIat6s0"
```

---

## 🧪 Paso 5: Probar el bot

1. En "Consoles" → "Bash", ejecuta:
   ```bash
   cd ~/telegram_bot
   python3.9 news_bot.py
   ```

2. Deberías ver los logs del bot iniciando
3. Presiona `Ctrl+C` para detenerlo

**Si hay errores:**
- Verifica que todas las dependencias estén instaladas
- Verifica que las variables de entorno estén correctas
- Revisa los mensajes de error

---

## ⏰ Paso 6: Configurar tarea programada (IMPORTANTE)

Para que el bot se ejecute automáticamente cada hora:

1. **Ve a "Tasks"** (en el menú superior)
2. **Click en "Create a new scheduled task"**
3. **Configura así:**

   **Command:**
   ```
   cd ~/telegram_bot && python3.9 news_bot.py --run-once
   ```

   **Or:** Si el bot no tiene modo `--run-once`, usa este script wrapper:

   **Command:**
   ```
   cd ~/telegram_bot && timeout 3300 python3.9 news_bot.py || true
   ```
   (Esto ejecuta el bot por máximo 55 minutos, luego se detiene)

   **Hour:** (deja en blanco para cada hora)
   
   **Minute:** `0` (ejecuta al inicio de cada hora)

4. **Activa la tarea:** Marca el checkbox "Enabled"
5. **Click en "Save"**

---

## 🔄 Alternativa: Script de ejecución única

Como PythonAnywhere ejecuta tareas cada hora, necesitamos modificar el bot para que:
- Se ejecute una vez
- Publique noticias
- Responda mensajes pendientes
- Se cierre después

### Crear script wrapper

1. Crea un archivo `run_task.py` en `~/telegram_bot/`:

```python
#!/usr/bin/env python3
"""
Wrapper para ejecutar el bot una vez (para tareas programadas)
"""
import os
import sys
import time
from news_bot import *

# Cargar variables de entorno desde .env si existe
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Ejecutar el bot por un tiempo limitado (55 minutos)
# Esto permite que PythonAnywhere lo ejecute cada hora
START_TIME = time.time()
MAX_RUNTIME = 55 * 60  # 55 minutos

def run_limited():
    global ADMIN_ID
    log("=" * 50)
    log("🤖 Bot 5.0: Scheduled Task Mode (PythonAnywhere)")
    log("=" * 50)

    if not TELEGRAM_BOT_TOKEN:
        log("ERROR: TELEGRAM_BOT_TOKEN environment variable not set!")
        return

    if not GEMINI_API_KEY:
        log("ERROR: GEMINI_API_KEY environment variable not set!")
        return
        
    log(f"Bot Token: {TELEGRAM_BOT_TOKEN[:10]}...")
    log(f"Channel: {TELEGRAM_CHANNEL}")
    log(f"Max runtime: {MAX_RUNTIME/60} minutes")
    log("=" * 50)
    
    history = load_history()
    log(f"👑 System Admin: {ADMIN_ID}")
    
    last_news_check = time.time() - CHECK_INTERVAL
    
    # Ejecutar por tiempo limitado
    while time.time() - START_TIME < MAX_RUNTIME:
        try:
            current_time = time.time()
            
            # 1. Poll for chat messages
            process_updates(history)
            
            # 2. Check news (cada hora, pero como se ejecuta cada hora, siempre publicará)
            if current_time - last_news_check >= CHECK_INTERVAL:
                log(f"Time for news check. Last check was {int(current_time - last_news_check)} seconds ago.")
                fetch_and_post_news(history)
                last_news_check = current_time
            
            time.sleep(POLL_INTERVAL)
            
            # Verificar tiempo restante
            elapsed = time.time() - START_TIME
            if elapsed >= MAX_RUNTIME:
                log(f"⏰ Maximum runtime reached ({MAX_RUNTIME/60} minutes). Exiting...")
                break
                
        except KeyboardInterrupt:
            log("Bot stopped by user")
            break
        except Exception as e:
            log(f"Critical Loop Error: {e}")
            log("Retrying in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    run_limited()
```

2. **Actualiza la tarea programada:**

   **Command:**
   ```
   cd ~/telegram_bot && python3.9 run_task.py
   ```

---

## ✅ Paso 7: Verificar que funciona

1. **Espera a la siguiente hora** (o configura para ejecutar en el próximo minuto para probar)
2. **Ve a "Tasks"** y verifica que la tarea se ejecutó
3. **Revisa los logs:**
   - Ve a "Files" → `~/telegram_bot/bot.log`
   - O ejecuta en consola: `tail -f ~/telegram_bot/bot.log`
4. **Prueba el bot:** Envía un mensaje en Telegram

---

## 📊 Estructura de archivos en PythonAnywhere

```
~/telegram_bot/
├── news_bot.py          (código principal)
├── run_task.py          (wrapper para tareas programadas - opcional)
├── requirements.txt     (dependencias)
├── .env                 (variables de entorno - OPCIONAL)
├── posted_articles.json (historial - se crea automáticamente)
└── bot.log             (logs - se crea automáticamente)
```

---

## 🔍 Monitoreo

### Ver logs en tiempo real
En consola Bash:
```bash
tail -f ~/telegram_bot/bot.log
```

### Ver estado de tareas
- Ve a "Tasks" en el dashboard
- Verás el historial de ejecuciones
- Click en una ejecución para ver logs

---

## ⚙️ Configuración Avanzada

### Ejecutar más frecuentemente (plan de pago)

Con el plan Hacker ($5/mes), puedes ejecutar tareas cada minuto:

1. Ve a "Tasks"
2. Cambia el intervalo de hora a minuto
3. Configura para ejecutar cada 15-30 minutos

---

## 🆘 Troubleshooting

### Error: "Module not found"
```bash
pip3.9 install --user nombre_del_modulo
```

### Error: "Permission denied"
Los archivos en PythonAnywhere no necesitan permisos especiales, pero verifica que puedas leerlos.

### El bot no publica nada
1. Verifica los logs: `cat ~/telegram_bot/bot.log`
2. Verifica que la tarea se esté ejecutando en "Tasks"
3. Verifica las variables de entorno

### El bot se ejecuta pero no responde
- Verifica que `TELEGRAM_BOT_TOKEN` esté correcto
- Verifica que el bot tenga permisos en el canal

---

## 💡 Tips

1. **Backup del historial:** Descarga `posted_articles.json` periódicamente
2. **Logs:** Los logs se guardan en `bot.log`, revisa si hay errores
3. **Actualizar código:** Simplemente sube el nuevo `news_bot.py` y se aplicará en la próxima ejecución

---

## ✅ Checklist Final

- [ ] Cuenta creada en PythonAnywhere
- [ ] Archivos subidos a `~/telegram_bot/`
- [ ] Dependencias instaladas (`pip3.9 install --user ...`)
- [ ] Variables de entorno configuradas (`.env` o en código)
- [ ] Bot probado manualmente (`python3.9 news_bot.py`)
- [ ] Tarea programada creada y activada
- [ ] Bot funcionando y publicando noticias

---

## 🎉 ¡Listo!

Tu bot ahora funcionará **automáticamente cada hora** en PythonAnywhere, incluso con tu Mac apagado.

**Frecuencia:**
- ✅ Se ejecuta cada hora (al inicio de cada hora)
- ✅ Publica noticias nuevas
- ✅ Responde mensajes pendientes
- ✅ Funciona 24/7 sin necesidad de tener tu Mac encendido

