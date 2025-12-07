# ☁️ Guía de Despliegue en la Nube - Bot 24/7

Esta guía te ayudará a desplegar tu bot de Telegram en la nube para que funcione **24/7 incluso con tu ordenador apagado**.

## 🎯 Opciones Recomendadas (Gratuitas o Muy Baratas)

### 🆓 Opción 1: Render (GRATIS - Recomendado)

**Render** ofrece hosting gratuito para workers que ejecutan indefinidamente.

#### Pasos:

1. **Crear cuenta en Render**
   - Ve a: https://render.com
   - Regístrate con GitHub (recomendado) o email

2. **Conectar repositorio**
   - Si tienes el código en GitHub, conecta el repositorio
   - O sube el código directamente

3. **Crear nuevo Web Service**
   - Click en "New" → "Background Worker"
   - Nombre: `telegram-tech-news-bot`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python3 news_bot.py`

4. **Configurar variables de entorno**
   - En "Environment Variables", añade:
     - `TELEGRAM_BOT_TOKEN` = tu token del bot
     - `GEMINI_API_KEY` = tu API key de Gemini

5. **Desplegar**
   - Click en "Create Background Worker"
   - ¡Listo! El bot estará funcionando 24/7

**Costo:** GRATIS (con algunas limitaciones) o $7/mes para plan ilimitado

---

### 🆓 Opción 2: Railway (GRATIS con límites)

Railway ofrece $5 gratis al mes, suficiente para un bot simple.

#### Pasos:

1. **Crear cuenta**
   - Ve a: https://railway.app
   - Regístrate con GitHub

2. **Nuevo proyecto**
   - "New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio

3. **Configurar**
   - Railway detectará automáticamente Python
   - Añade variables de entorno en "Variables":
     - `TELEGRAM_BOT_TOKEN`
     - `GEMINI_API_KEY`

4. **Desplegar**
   - Click en "Deploy"
   - El bot se desplegará automáticamente

**Costo:** $5 gratis/mes, luego $5/mes

---

### 🆓 Opción 3: Fly.io (GRATIS)

Fly.io tiene un plan gratuito generoso.

#### Pasos:

1. **Instalar Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Inicializar app**
   ```bash
   cd telegram_tech_news
   fly launch
   ```

4. **Configurar secrets**
   ```bash
   fly secrets set TELEGRAM_BOT_TOKEN=tu_token
   fly secrets set GEMINI_API_KEY=tu_api_key
   ```

5. **Desplegar**
   ```bash
   fly deploy
   ```

**Costo:** GRATIS (plan gratuito generoso)

---

### 💰 Opción 4: DigitalOcean App Platform ($5/mes)

#### Pasos:

1. **Crear cuenta en DigitalOcean**
   - Ve a: https://www.digitalocean.com

2. **Nuevo App**
   - "Create" → "Apps"
   - Conecta tu repositorio GitHub

3. **Configurar**
   - Tipo: Worker
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python3 news_bot.py`
   - Añade variables de entorno

4. **Desplegar**
   - Click en "Create Resources"

**Costo:** $5/mes

---

### 🆓 Opción 5: PythonAnywhere (Gratis con limitaciones)

**Limitación:** Solo puede ejecutarse en horarios programados (tareas), no 24/7 continuo.

#### Pasos:

1. **Registrarse**
   - Ve a: https://www.pythonanywhere.com

2. **Subir código**
   - En "Files", crea carpeta y sube `news_bot.py` y `requirements.txt`

3. **Instalar dependencias**
   - En "Consoles" → "Bash":
   ```bash
   pip3.9 install --user feedparser requests google-generativeai beautifulsoup4
   ```

4. **Configurar tarea programada**
   - En "Tasks", crea una tarea que ejecute el bot cada hora
   - **Nota:** No es 24/7 continuo, pero funciona cada hora

**Costo:** GRATIS

---

## 🔧 Preparación del Código

El código ya está preparado para la nube. Solo necesitas:

1. **Variables de entorno**: El bot lee `TELEGRAM_BOT_TOKEN` y `GEMINI_API_KEY` del entorno automáticamente
2. **Archivos incluidos**: 
   - `Procfile` (para Heroku/Render) ✅
   - `Dockerfile` (para Docker) ✅
   - `render.yaml` (para Render) ✅
   - `railway.json` (para Railway) ✅
   - `requirements.txt` (dependencias) ✅

**IMPORTANTE:** No necesitas modificar el código. El bot ya está configurado para leer variables de entorno desde `os.getenv()`.

## 📋 Checklist de Deployment

- [ ] Cuenta creada en el servicio cloud elegido
- [ ] Código subido (GitHub o directamente)
- [ ] Variables de entorno configuradas:
  - [ ] `TELEGRAM_BOT_TOKEN`
  - [ ] `GEMINI_API_KEY`
- [ ] Bot desplegado y funcionando
- [ ] Verificar logs para confirmar que está funcionando

## 🧪 Verificar que Funciona

Después del deployment, verifica:

1. **Logs del servicio**: Revisa los logs para ver si el bot está corriendo
2. **Mensaje de prueba**: Envía un mensaje al bot en Telegram
3. **Monitoreo**: Revisa que esté publicando noticias según el intervalo configurado

## 📊 Recomendación Final

**Para empezar:** Render (gratis) o Railway (con $5 gratis/mes)
**Para producción:** DigitalOcean App Platform ($5/mes) o VPS propio

---

## 🆘 Troubleshooting

**El bot no inicia:**
- Verifica que las variables de entorno estén correctamente configuradas
- Revisa los logs del servicio para ver errores
- Asegúrate de que `requirements.txt` tenga todas las dependencias

**El bot se detiene:**
- Algunos servicios gratuitos pueden pausar workers inactivos
- Considera actualizar a un plan de pago si necesitas 24/7 garantizado

**Errores de importación:**
- Verifica que todas las dependencias estén en `requirements.txt`
- Algunos servicios requieren versión específica de Python (verifica `runtime.txt`)

