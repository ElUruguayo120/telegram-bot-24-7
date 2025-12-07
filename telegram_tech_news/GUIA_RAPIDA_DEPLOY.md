# 🚀 Guía Rápida: Subir el Bot a la Nube (5 minutos)

## 📍 Situación Actual

✅ **El bot está funcionando en tu Mac local**
- Funciona mientras el Mac esté encendido
- ❌ Se detiene si apagas el ordenador

## 🎯 Objetivo

Subir el bot a un servidor en la nube para que funcione **24/7 incluso con tu Mac apagado**.

---

## ⚡ Opción Más Rápida: Render (GRATIS)

### Paso 1: Crear cuenta (1 minuto)
1. Ve a: https://render.com
2. Click en "Get Started for Free"
3. Regístrate con GitHub (recomendado) o email

### Paso 2: Subir código (2 minutos)

**Opción A: Si tienes GitHub**
1. Crea un repositorio en GitHub
2. Sube todos los archivos del proyecto:
   ```bash
   cd "/Users/marcelo/prueba a programar con python /telegram_tech_news"
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/TU_USUARIO/telegram-tech-news.git
   git push -u origin main
   ```

**Opción B: Sin GitHub (subir directamente)**
1. En Render, click "New" → "Background Worker"
2. Selecciona "Build and deploy from a Git repository" o "Deploy existing image"
3. Si no tienes Git, puedes usar "Manual Deploy" y subir los archivos

### Paso 3: Configurar en Render (2 minutos)
1. **Nombre del servicio**: `telegram-tech-news-bot`
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python3 news_bot.py`
4. **Variables de entorno** (IMPORTANTE):
   - Click en "Environment"
   - Añade:
     - `TELEGRAM_BOT_TOKEN` = `6665925860:AAHa-Eu8xKhece83HaKEsHTB8x8CGF61Czk`
     - `GEMINI_API_KEY` = `AIzaSyAYgke20w4fNeZL_zK3wm8r19NgbIat6s0`
5. Click en "Create Background Worker"

### Paso 4: Verificar (1 minuto)
1. Espera a que termine el deployment (2-3 minutos)
2. Ve a "Logs" para ver si está funcionando
3. Prueba enviando un mensaje al bot en Telegram

---

## 🎉 ¡Listo!

Una vez desplegado:
- ✅ El bot funcionará 24/7
- ✅ Funciona aunque apagues tu Mac
- ✅ Se reinicia automáticamente si hay errores
- ✅ Puedes ver los logs en Render

---

## 🔄 Actualizar el Bot

Si haces cambios:
1. Sube los cambios a GitHub (si usas Git)
2. Render se actualizará automáticamente
3. O haz "Manual Deploy" en Render

---

## 📊 Otras Opciones Rápidas

### Railway (También fácil)
1. Ve a: https://railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Añade variables de entorno
4. ¡Listo!

### Fly.io (Con Docker)
1. Instala: `curl -L https://fly.io/install.sh | sh`
2. `fly launch`
3. `fly secrets set TELEGRAM_BOT_TOKEN=tu_token`
4. `fly secrets set GEMINI_API_KEY=tu_key`
5. `fly deploy`

---

## ⚠️ Importante

**NO subas el archivo `.env` a GitHub** - ya está en `.gitignore`

Las variables de entorno se configuran directamente en la plataforma cloud.

---

## 🆘 ¿Problemas?

- **El bot no inicia**: Revisa los logs en Render
- **Error de variables**: Verifica que estén bien escritas en "Environment"
- **No encuentra dependencias**: Asegúrate de que `requirements.txt` esté completo

