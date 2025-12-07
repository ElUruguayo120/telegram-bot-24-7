# 🚀 GUÍA RÁPIDA: Subir Bot a PythonAnywhere

## 📋 PASO 1: Crear Cuenta (5 minutos)

1. **Ve a:** https://www.pythonanywhere.com
2. **Click en:** "Pricing & signup" (arriba derecha)
3. **Elige:** Plan "Beginner" (GRATIS)
4. **Registra tu cuenta:**
   - Username: (elige uno, ej: `marcelotech`)
   - Email: tu email
   - Password: tu contraseña
5. **Confirma tu email** y haz login

---

## 📂 PASO 2: Subir Archivos (10 minutos)

### Opción A: Interfaz Web (Más fácil)

1. **Abre "Files"** (menú superior)
2. **Crea carpeta:** `telegram_bot`
3. **Entra a la carpeta** `telegram_bot`
4. **Sube estos archivos** (uno por uno):
   - ✅ `news_bot.py`
   - ✅ `run_task.py`
   - ✅ `requirements.txt`
   - ✅ `.env`

### Opción B: Consola Bash (Más rápido)

1. **Abre "Consoles"** → "Bash"
2. **Ejecuta estos comandos:**

```bash
# Crear carpeta
mkdir -p ~/telegram_bot
cd ~/telegram_bot

# Crear archivo .env con tus credenciales
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=6665925860:AAHa-Eu8xKhece83HaKEsHTB8x8CGF61Czk
GEMINI_API_KEY=AIzaSyAYgke20w4fNeZL_zK3wm8r19NgbIat6s0
EOF

# Crear requirements.txt
cat > requirements.txt << 'EOF'
feedparser
requests
google-generativeai
beautifulsoup4
EOF
```

3. **Sube `news_bot.py` y `run_task.py`** usando el editor web:
   - Ve a "Files" → `telegram_bot`
   - Click en "Upload a file"
   - Sube ambos archivos

---

## 🔧 PASO 3: Instalar Dependencias (2 minutos)

En la **consola Bash**:

```bash
cd ~/telegram_bot
pip3.10 install --user feedparser requests google-generativeai beautifulsoup4
```

**Espera** a que termine la instalación (puede tardar 1-2 minutos)

---

## 🧪 PASO 4: Probar el Bot (2 minutos)

```bash
cd ~/telegram_bot
python3.10 run_task.py
```

**Deberías ver:**
- ✅ "Bot 5.0: Scheduled Task Mode"
- ✅ Logs de inicio
- ✅ "Checking for news..."

**Presiona `Ctrl+C`** para detener el bot

---

## ⏰ PASO 5: Configurar Tarea Automática (3 minutos)

1. **Ve a "Tasks"** (menú superior)
2. **Scroll down** hasta "Scheduled tasks"
3. **Click en "Create a new scheduled task"**
4. **Configura:**
   - **Hour:** (déjalo vacío)
   - **Minute:** `0`
   - **Command:** 
     ```
     cd ~/telegram_bot && python3.10 run_task.py
     ```
5. **Click en "Create"**
6. **Verifica** que aparezca en la lista con un ✓ verde

---

## ✅ PASO 6: Verificar que Funciona

### Inmediatamente:
1. **Ve a "Tasks"**
2. **Click en "Run now"** (botón junto a tu tarea)
3. **Espera 10 segundos**
4. **Revisa los logs:**
   ```bash
   tail -20 ~/telegram_bot/bot.log
   ```

### En 1 hora:
1. **Espera a la siguiente hora** (ej: si son 14:30, espera hasta las 15:00)
2. **Ve a tu canal de Telegram**
3. **Deberías ver** noticias nuevas publicadas

---

## 📊 Monitoreo

### Ver logs en tiempo real:
```bash
tail -f ~/telegram_bot/bot.log
```

### Ver historial de ejecuciones:
- Ve a "Tasks"
- Verás cada ejecución con fecha/hora
- Click en una para ver los logs

### Ver archivos creados:
```bash
ls -lh ~/telegram_bot/
```

---

## 🆘 Solución de Problemas

### Error: "Module not found"
```bash
pip3.10 install --user nombre_del_modulo
```

### El bot no publica nada
1. Verifica los logs: `cat ~/telegram_bot/bot.log`
2. Verifica que la tarea esté activada en "Tasks"
3. Ejecuta manualmente: `python3.10 run_task.py`

### Error de credenciales
1. Verifica el archivo `.env`:
   ```bash
   cat ~/telegram_bot/.env
   ```
2. Asegúrate de que tenga las dos líneas correctas

---

## 🎉 ¡Listo!

Tu bot ahora está funcionando 24/7 en PythonAnywhere:

- ✅ Se ejecuta **cada hora** automáticamente
- ✅ Publica noticias nuevas
- ✅ Responde mensajes con IA
- ✅ Funciona incluso con tu Mac apagado
- ✅ **100% GRATIS**

---

## 📞 Comandos Útiles

```bash
# Ver logs
tail -f ~/telegram_bot/bot.log

# Ver últimas 50 líneas
tail -50 ~/telegram_bot/bot.log

# Ver artículos publicados
cat ~/telegram_bot/posted_articles.json | python3 -m json.tool | tail -20

# Reiniciar el bot manualmente
cd ~/telegram_bot && python3.10 run_task.py

# Ver espacio usado
du -sh ~/telegram_bot/
```

---

## 🔄 Actualizar el Bot

Si haces cambios en tu código local:

1. **Ve a "Files"** → `telegram_bot`
2. **Click en el archivo** que quieres actualizar
3. **Click en "Upload a file"**
4. **Selecciona el nuevo archivo** (sobrescribirá el anterior)
5. **Listo!** Se aplicará en la próxima ejecución

---

**Tiempo total:** ~20-25 minutos  
**Costo:** $0 (GRATIS para siempre)
