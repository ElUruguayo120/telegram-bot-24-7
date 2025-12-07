
# ☁️ SERVIDOR MAESTRO 24/7 (Guía Definitiva)

He creado la arquitectura de **"Servidor Unificado"**.
Esto significa que ahora tienes UN SOLO programa (`unified_server.py`) que hace todo:
1. Mantiene el bot despierto (Flask).
2. Busca noticias automáticamente (Scheduler).
3. Responde chats (IA).

---

## 🚀 OPCION 1: Railway (Recomendado para 24/7 REAL)

Railway.app es mucho mejor que PythonAnywhere para bots "infinitos" porque te da un servidor Docker real.

1. Sube este código a **GitHub**.
2. Ve a **Railway.app** -> "New Project" -> "Deploy from GitHub repo".
3. Railway leerá automáticamente el archivo `Procfile` que creé.
4. **¡LISTO!** Tu bot correrá para siempre.

---

## 🐍 OPCION 2: PythonAnywhere (Si prefieres quedarte)

Si te quedas en PythonAnywhere, usa la **Web App**:

1. Ve a la pestaña **Web**.
2. Configura el "WSGI configuration file" para apuntar al nuevo servidor:

```python
import sys
path = '/home/tucousuario/telegram_bot'
if path not in sys.path:
    sys.path.append(path)

from telegram_tech_news.unified_server import app as application
```

⚠️ **NOTA:** En PythonAnywhere, el "Scheduler" (noticias automáticas) que va dentro del servidor a veces se duerme si nadie visita la web.
Por eso, en PythonAnywhere es MEJOR usar la pestaña **"Tasks"** por separado (como expliqué en la guía anterior).

Pero si usas **Railway** o cualquier VPS, el archivo `unified_server.py` es la SOLUCIÓN DEFINITIVA.

---

## 🔧 Archivos Clave Creados
- `unified_server.py`: El cerebro que hace todo.
- `Procfile`: La instrucción para que la nube sepa cómo arrancar.
- `requirements.txt`: Lista de motores necesarios.
