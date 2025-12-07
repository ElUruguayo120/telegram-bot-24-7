
# 🚀 Guía Definitiva: Bot Indestructible (Webhook + Scheduled Task)

Si tu bot anterior **se detenía**, era porque las consolas gratuitas de PythonAnywhere **siempre se cierran**.
Para que dure **para siempre (24/7)**, cambiamos la estrategia a **Web App (Webhook)**.

Esta es la forma "Profesional" que usan los expertos.

---

## 🛠️ PASO 1: Subir los nuevos archivos

1. Ve a **Files** en PythonAnywhere.
2. Sube estos 4 archivos nuevos que he creado:
   - `telegram_tech_news/bot_config.py`
   - `telegram_tech_news/bot_utils.py`
   - `telegram_tech_news/rss_job.py`
   - `telegram_tech_news/flask_webhook.py`
   - y tu `.env` (si no está ya).

*(Puedes borrar el viejo `news_bot.py` si quieres).*

---

## 🌐 PASO 2: Configurar la Web App (Para Chat 24/7)

Esto mantendrá al bot "escuchando" siempre.

1. Ve a la pestaña **Web**.
2. Click **"Add a new web app"**.
3. Dale **Next** -> Selecciona **Flask** -> Selecciona **Python 3.10**.
4. En "Path", borra lo que hay y pon la ruta a tu archivo nuevo.
   - **IMPORTANTE:** Aquí pythonanywhere te pedirá un archivo `flask_app.py` por defecto. Déjalo crearse.
5. Una vez creada la app, baja a la sección **"Code"**.
   - Click en el link que dice **"WSGI configuration file"** (ej: `/var/www/tuchico_pythonanywhere_com_wsgi.py`).
6. Borra TODO el contenido de ese archivo y pega esto:

```python
import sys
import os

# Ajusta esta ruta a donde subiste tu carpeta
path = '/home/tucousuario/telegram_bot/telegram_tech_news'
if path not in sys.path:
    sys.path.append(path)

# Importar la app Flask
from flask_webhook import app as application
```
*(Cambia `tucousuario` por tu usuario real de PythonAnywhere y la ruta si es distinta).*

7. Dale a **Save**.
8. Vuelve a la pestaña **Web** y dale al botón verde gigantesco **"Reload"**.

---

## 🔗 PASO 3: Conectar Telegram (Webhook)

Ahora dile a Telegram que envíe los mensajes a tu nueva Web App.

1. Abre una pestaña nueva en tu navegador.
2. Escribe esta dirección (reemplaza con tus datos):
   `http://<tu-usuario>.pythonanywhere.com/set_webhook`
3. Si ves "Webhook setup result: True", **¡FELICIDADES!** 🎉
   Tu bot ahora responde instantáneamente y **NUNCA SE APAGARÁ**.

---

## ⏰ PASO 4: Noticias Automáticas (RSS)

Como las noticias no son "respuestas", necesitamos una tarea que las busque cada hora.

1. Ve a la pestaña **Tasks**.
2. En "Scheduled tasks", pon este comando:
   ```bash
   python3.10 /home/tucousuario/telegram_bot/telegram_tech_news/rss_job.py
   ```
3. Configura para que corra **Hourly** (cada hora).
4. Dale a **Create**.

---

## ✅ Resumen del "Control Total"

Ahora tienes un sistema híbrido indestructible:
1. **Web App:** Maneja el Chat y la IA. Siempre despierta.
2. **Tasks:** Maneja las noticias RSS. Se despierta, trabaja y duerme (ahorrando recursos).

¡Nunca más tendrás que reiniciar consolas! 🚀
