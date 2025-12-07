# 🚀 Guía para Poner en Marcha el Bot

## ⚠️ Estado Actual

El bot está **instalado y configurado** correctamente, pero el **token de Telegram ha expirado o es inválido**.

### ✅ Lo que está funcionando:
- ✅ Entorno virtual Python activado
- ✅ Todas las dependencias instaladas
- ✅ Código del bot sin errores
- ✅ Archivo `.env` configurado
- ✅ Sistema de logging funcionando

### ❌ Lo que necesita corrección:
- ❌ Token de Telegram inválido (Error 401: Unauthorized)

---

## 🔧 Solución: Obtener un Nuevo Token

### Paso 1: Abrir Telegram

1. Abre la aplicación de Telegram en tu teléfono o computadora
2. Busca el contacto **@BotFather**
3. Inicia una conversación con él

### Paso 2: Crear o Recuperar el Bot

**Opción A: Si ya tienes un bot creado**
```
Envía a @BotFather:
/mybots

Selecciona tu bot de la lista
Selecciona "API Token"
Copia el token que te muestre
```

**Opción B: Si necesitas crear un nuevo bot**
```
Envía a @BotFather:
/newbot

Sigue las instrucciones:
1. Nombre del bot (ej: "Tech News Bot")
2. Username del bot (debe terminar en "bot", ej: "technews_portal_bot")

@BotFather te dará un token como:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Paso 3: Actualizar el Token

Una vez tengas el nuevo token, actualiza el archivo `.env`:

```bash
cd "/Users/marcelo/prueba a programar con python /telegram_tech_news"
nano .env
```

Edita la línea:
```
TELEGRAM_BOT_TOKEN=TU_NUEVO_TOKEN_AQUI
```

Guarda con `Ctrl+O`, Enter, `Ctrl+X`

### Paso 4: Reiniciar el Bot

```bash
# Si el bot está corriendo, detenerlo primero
# Presiona Ctrl+C en la terminal donde está corriendo

# Luego iniciar de nuevo
source .venv/bin/activate
python3 news_bot.py
```

---

## 📊 Resumen de Funciones del Bot

He creado un **análisis completo** de todas las funciones en el archivo:
📄 **`ANALISIS_FUNCIONES.md`**

### Funciones Principales:

1. **📰 RSS Feeds** - Monitorea 10+ fuentes de noticias tech
2. **🤖 IA Gemini** - Respuestas inteligentes con Google AI
3. **⏸️ Sistema de Pausa** - Control manual del bot
4. **🔍 Detección de Duplicados** - Evita publicar la misma noticia
5. **💬 Comandos** - /start, /pause, /resume, /status, /last, /help
6. **📊 Gráficas** - Estadísticas de actividad
7. **💾 Historial Persistente** - Guarda estado entre reinicios
8. **📝 Logging** - Registro detallado de eventos
9. **🔄 Polling** - Recepción continua de mensajes
10. **📤 Envío a Telegram** - Publicación automática en canal
11. **🧠 Respuestas con IA** - Chat inteligente con usuarios
12. **⚙️ Variables de Entorno** - Configuración flexible
13. **📦 Dependencias Opcionales** - Funciona aunque falten librerías
14. **🔁 Loop Robusto** - Recuperación automática de errores

---

## 🎯 Comandos Disponibles

Una vez el bot esté funcionando, puedes usar:

| Comando | Descripción |
|---------|-------------|
| `/start` | Mostrar menú de ayuda |
| `/pause` | Pausar publicación de noticias |
| `/resume` | Reanudar publicación de noticias |
| `/status` | Ver estadísticas del bot |
| `/last` | Ver últimas 5 noticias publicadas |
| `/help` | Mostrar ayuda |
| `Cualquier texto` | El bot responderá con IA Gemini |

---

## 🔐 Configuración del Canal

### Paso 1: Crear o Usar un Canal

1. En Telegram, crea un canal público o usa uno existente
2. El username del canal debe ser como: `@Portal_tech2` (o el que prefieras)

### Paso 2: Agregar el Bot como Administrador

1. Ve a tu canal
2. Toca el nombre del canal → Administradores
3. Agregar Administrador
4. Busca tu bot por su username
5. Dale permisos de "Publicar mensajes"

### Paso 3: Actualizar el Canal en el Código (si es diferente)

Si tu canal no es `@Portal_tech2`, edita `news_bot.py`:

```python
TELEGRAM_CHANNEL = "@TU_CANAL_AQUI"
```

---

## 🧪 Pruebas

### Verificar Conexión del Bot

```bash
python3 check_bot_status.py
```

Deberías ver:
```
✅ Bot conectado correctamente!
   • Nombre: Tech News Bot
   • Username: @tu_bot
   • ID: 123456789
   • Es bot: True
```

### Prueba Completa

```bash
python3 test_bot.py
```

### Envío Manual de Mensaje

```bash
python3 quick_test.py
```

---

## 🚀 Ejecución

### Modo Desarrollo (Local)

```bash
cd "/Users/marcelo/prueba a programar con python /telegram_tech_news"
source .venv/bin/activate
python3 news_bot.py
```

El bot se ejecutará continuamente hasta que presiones `Ctrl+C`.

### Modo Producción (Background)

```bash
# Opción 1: Con nohup
nohup python3 news_bot.py > output.log 2>&1 &

# Opción 2: Con screen
screen -S telegram_bot
python3 news_bot.py
# Presiona Ctrl+A, luego D para desconectar
# Para reconectar: screen -r telegram_bot

# Opción 3: Con tmux
tmux new -s telegram_bot
python3 news_bot.py
# Presiona Ctrl+B, luego D para desconectar
# Para reconectar: tmux attach -t telegram_bot
```

---

## 📝 Logs

### Ver logs en tiempo real

```bash
tail -f bot.log
```

### Ver últimas 50 líneas

```bash
tail -50 bot.log
```

### Buscar errores

```bash
grep -i error bot.log
```

---

## 🐛 Solución de Problemas

### Error 401: Unauthorized
**Causa:** Token inválido o expirado  
**Solución:** Obtener nuevo token de @BotFather (ver arriba)

### Error 400: Bad Request
**Causa:** Formato de mensaje incorrecto  
**Solución:** Revisar que el HTML esté bien formado

### Error 403: Forbidden
**Causa:** El bot no tiene permisos en el canal  
**Solución:** Agregar el bot como administrador del canal

### No se publican noticias
**Causa:** Bot pausado o feeds RSS no disponibles  
**Solución:** Enviar `/resume` al bot o verificar conexión a internet

### IA no responde
**Causa:** API Key de Gemini inválida o sin cuota  
**Solución:** Verificar `GEMINI_API_KEY` en `.env`

---

## 📚 Archivos Importantes

| Archivo | Descripción |
|---------|-------------|
| `news_bot.py` | Código principal del bot |
| `ANALISIS_FUNCIONES.md` | Análisis completo de funciones |
| `README.md` | Documentación general |
| `.env` | Variables de entorno (sensible) |
| `posted_articles.json` | Historial de noticias |
| `bot.log` | Registro de eventos |
| `requirements.txt` | Dependencias Python |
| `check_bot_status.py` | Script de diagnóstico |

---

## 🎓 Próximos Pasos

1. ✅ **Obtener nuevo token** de @BotFather
2. ✅ **Actualizar `.env`** con el nuevo token
3. ✅ **Verificar conexión** con `check_bot_status.py`
4. ✅ **Configurar canal** y agregar bot como admin
5. ✅ **Iniciar el bot** con `python3 news_bot.py`
6. ✅ **Probar comandos** enviando `/start` al bot
7. ✅ **Revisar logs** para confirmar que todo funciona

---

## 💡 Consejos

- 🔒 **Nunca compartas** tu token de bot públicamente
- 📊 **Revisa los logs** regularmente para detectar problemas
- ⏰ **Ajusta CHECK_INTERVAL** en `news_bot.py` si quieres chequeos más frecuentes
- 🌐 **Agrega más feeds RSS** en la lista `RSS_FEEDS`
- 🤖 **Configura Gemini API** para habilitar respuestas con IA

---

## 📞 Soporte

Si tienes problemas:

1. Revisa `bot.log` para errores específicos
2. Ejecuta `check_bot_status.py` para diagnosticar
3. Verifica que todas las dependencias estén instaladas
4. Confirma que el token y el canal sean correctos

---

**¡El bot está listo para funcionar una vez actualices el token!** 🚀

*Última actualización: 2025-12-06*
