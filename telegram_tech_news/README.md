# 🤖 Telegram Tech News Bot

Bot automático que publica las últimas noticias de tecnología en un canal de Telegram usando RSS feeds e inteligencia artificial.

## 🚀 Características

- 📰 **RSS Feeds**: Monitorea 10+ fuentes de noticias tech en español e inglés
- 🎙️ **Podcasts**: Publica episodios de podcasts tech
- 🤖 **IA Gemini**: Mejora automática de textos y respuestas inteligentes
- ⏱️ **Alarmas**: Sistema de alarmas configurables
- 📊 **Gráficas**: Estadísticas de actividad en tiempo real
- 🎛️ **Controles**: Botones inline para pausar/reanudar
- 🌐 **Web Dashboard**: Panel de control web (opcional)

## 📋 Requisitos

- Python 3.9+
- Token de bot Telegram
- API Key de Google Gemini (opcional, para IA)
- Conexión a internet

## ⚙️ Instalación

### 1. Clonar o descargar el proyecto

```bash
cd ~/telegram_tech_news
```

### 2. Crear entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```bash
TELEGRAM_BOT_TOKEN=tu_token_aqui
GEMINI_API_KEY=tu_api_key_aqui
```

## 🧪 Pruebas

### Prueba básica de conexión

```bash
python3 test_bot.py
```

### Prueba en múltiples canales

```bash
python3 test_both.py
```

### Envío manual de mensaje

```bash
python3 quick_test.py
```

## 🏃 Ejecución

### Modo local (desarrollo)

```bash
export TELEGRAM_BOT_TOKEN="tu_token"
export GEMINI_API_KEY="tu_api_key"
python3 news_bot.py
```

### Modo PythonAnywhere (producción)

1. Sube los archivos a PythonAnywhere
2. Crea una **Scheduled Task** en PythonAnywhere:
   - Comando: `/home/usuario/telegram_tech_news/run_task.py`
   - Hora: Cada hora (00:00)

3. O usa **Always-On Web App** para ejecución continua

## 📝 Comandos disponibles

### Comandos de usuario

- `/start` - Mostrar menú de ayuda
- `/pause` - Pausar el bot
- `/resume` - Reanudar el bot
- `/status` - Ver estado actual
- `/graph` - Ver gráfica de actividad
- `/last` - Últimas 5 noticias
- `/help` - Mostrar esta ayuda

### Botones inline

- ⏸️ Pausar Bot
- ▶️ Reanudar Bot
- 🔄 Forzar Chequeo
- 📊 Estado
- 📈 Gráfica
- ⏱️ Alarma 5m/15m/1h
- ⏹️ Detener Alarmas

## 📚 Feeds RSS

El bot monitorea estas fuentes:

**Español:**
- Xataka
- Genbeta
- Applesfera
- XatakaAndroid
- XatakaMóvil
- XatakaWindows
- ADSLZone
- MuyComputer
- RedesZone
- La Manzana Mordida

**Podcasts:**
- Mixx.io
- Simplecast
- iVoox

## 🛠️ Estructura del proyecto

```
telegram_tech_news/
├── news_bot.py              # Bot principal
├── run_task.py              # Wrapper para tareas programadas
├── web_app.py               # Dashboard web (opcional)
├── test_bot.py              # Suite de pruebas
├── test_both.py             # Prueba multi-canal
├── quick_test.py            # Prueba rápida
├── requirements.txt         # Dependencias Python
├── .env.example             # Ejemplo de configuración
├── .gitignore               # Archivos a ignorar en git
├── README.md                # Este archivo
└── posted_articles.json     # Historial (se crea automáticamente)
```

## 🔐 Seguridad

- Las credenciales se almacenan en `.env` (nunca en git)
- El archivo `.env` debe tener permisos 600
- Nunca compartas tu `TELEGRAM_BOT_TOKEN`

## 🐛 Solución de problemas

### El bot no responde
1. Verifica que el token sea válido: `python3 test_bot.py`
2. Verifica que el bot sea administrador del canal
3. Revisa el archivo `bot.log` para errores

### No se envían noticias
1. Comprueba la conexión a internet
2. Verifica los feeds RSS en `test_bot.py`
3. Revisa que el canal sea público

### Error de IA (Gemini)
1. Verifica que la API Key sea correcta
2. Que tenga cuota disponible en Google Cloud
3. Desactiva con `USE_AI_ENHANCEMENT=false` en `.env`

## 📖 Documentación adicional

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Google Gemini API](https://ai.google.dev/)
- [Feedparser Documentation](https://feedparser.readthedocs.io/)

## 📄 Licencia

Libre para uso personal y educativo.

## 👨‍💻 Autor

Bot de noticias tech desarrollado con ❤️

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**¿Preguntas?** Revisa el archivo `bot.log` o abre un issue.
