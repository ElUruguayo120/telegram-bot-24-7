# 🚀 Guía Simple: Bot 24/7 en PythonAnywhere

## ⚠️ IMPORTANTE
Cuando apagas tu Mac, el bot deja de funcionar porque se ejecuta localmente.
**Solución:** Desplegarlo en PythonAnywhere (servidor en la nube GRATIS)

---

## 📝 PASO 1: Crear Cuenta en PythonAnywhere

1. Ve a: **https://www.pythonanywhere.com**
2. Click en **"Pricing & signup"**
3. Selecciona el plan **"Beginner (Free)"**
4. Regístrate con tu email
5. ✅ **NO necesitas tarjeta de crédito**

---

## 📂 PASO 2: Subir tu Código

### Opción A: Subir archivos manualmente (MÁS FÁCIL)

1. **Accede al Dashboard** de PythonAnywhere
2. Click en **"Files"** (menú superior)
3. Click en **"Upload a file"**
4. Sube estos archivos desde tu Mac:
   - `news_bot.py`
   - `requirements.txt`
   - `.env` (con tus tokens)
   - `posted_articles.json` (opcional, para mantener historial)

### Opción B: Usar consola Bash

1. En el Dashboard, click en **"Consoles"** → **"Bash"**
2. Ejecuta estos comandos:

```bash
# Crear carpeta
mkdir -p ~/telegram_bot
cd ~/telegram_bot

# Crear archivo .env con tus tokens
nano .env
```

3. Pega esto en el archivo `.env`:
```
TELEGRAM_BOT_TOKEN=6665925860:AAHa-Eu8xKhece83HaKEsHTB8x8CGF61Czk
GEMINI_API_KEY=AIzaSyAYgke20w4fNeZL_zK3wm8r19NgbIat6s0
```

4. Guarda con `Ctrl+X`, luego `Y`, luego `Enter`

---

## 🔧 PASO 3: Instalar Dependencias

En la consola Bash de PythonAnywhere:

```bash
cd ~/telegram_bot
pip3.10 install --user feedparser requests google-generativeai beautifulsoup4
```

**Nota:** PythonAnywhere usa Python 3.10

---

## ⏰ PASO 4: Configurar Tarea Programada (CLAVE)

Esto hace que tu bot se ejecute automáticamente cada hora:

1. En el Dashboard, click en **"Tasks"**
2. En la sección **"Scheduled tasks"**, busca donde dice **"Enter command"**
3. Pega este comando:

```bash
cd ~/telegram_bot && timeout 3300 python3.10 news_bot.py || true
```

4. Configura el horario:
   - **Hour:** Deja en blanco (para ejecutar cada hora)
   - **Minute:** `0` (ejecuta al inicio de cada hora)

5. Click en **"Create"**

---

## 🧪 PASO 5: Probar que Funciona

### Prueba Manual (Opcional)

En la consola Bash:

```bash
cd ~/telegram_bot
python3.10 news_bot.py
```

Deberías ver los logs del bot. Presiona `Ctrl+C` para detenerlo.

### Verificar Tarea Programada

1. Espera a la siguiente hora en punto (ej: 01:00, 02:00, etc.)
2. Ve a **"Tasks"** en el Dashboard
3. Verás el historial de ejecuciones
4. Click en una ejecución para ver los logs

---

## 📊 PASO 6: Verificar en Telegram

1. Abre Telegram
2. Ve a tu canal `@Portal_tech2`
3. Espera a la siguiente hora
4. Deberías ver noticias nuevas publicadas automáticamente

---

## 🔍 Monitoreo y Logs

### Ver logs del bot

En consola Bash:

```bash
cd ~/telegram_bot
cat bot.log
```

O para ver en tiempo real:

```bash
tail -f ~/telegram_bot/bot.log
```

### Ver estado de tareas

- Ve a **"Tasks"** en el Dashboard
- Verás todas las ejecuciones recientes
- Verde = Exitosa
- Rojo = Error (click para ver detalles)

---

## 🆘 Solución de Problemas

### ❌ El bot no publica noticias

**Verifica:**
1. Que la tarea esté **activada** (checkbox marcado en Tasks)
2. Que el archivo `.env` tenga los tokens correctos
3. Los logs en `bot.log` para ver errores

**Comando para verificar:**
```bash
cd ~/telegram_bot
cat .env
```

### ❌ Error "Module not found"

Instala la dependencia faltante:
```bash
pip3.10 install --user nombre_del_modulo
```

### ❌ El bot no responde a mensajes

El bot en modo tarea programada solo:
- ✅ Publica noticias cada hora
- ✅ Responde mensajes pendientes cada hora
- ❌ NO responde instantáneamente (solo cada hora)

**Para respuestas instantáneas necesitas el plan de pago ($5/mes)**

---

## 📋 Checklist Final

- [ ] Cuenta creada en PythonAnywhere
- [ ] Archivos subidos (`news_bot.py`, `requirements.txt`, `.env`)
- [ ] Dependencias instaladas (`pip3.10 install --user ...`)
- [ ] Archivo `.env` con tokens correctos
- [ ] Tarea programada creada y activada
- [ ] Bot probado manualmente (opcional)
- [ ] Esperado 1 hora para verificar publicación automática

---

## ✅ ¡Listo!

Tu bot ahora funciona **24/7 en la nube**, incluso con tu Mac apagado.

**Frecuencia de ejecución:**
- 🕐 Cada hora en punto (00:00, 01:00, 02:00, etc.)
- 📰 Publica noticias nuevas
- 💬 Responde mensajes pendientes
- 🔄 Se ejecuta automáticamente sin intervención

---

## 💡 Consejos

1. **Backup:** Descarga `posted_articles.json` periódicamente para no perder historial
2. **Actualizar código:** Simplemente sube el nuevo `news_bot.py` y se aplicará en la próxima ejecución
3. **Logs:** Revisa `bot.log` regularmente para detectar errores
4. **Plan gratis:** Tiene limitaciones pero es perfecto para tu bot

---

## 🔄 Actualizar el Bot

Cuando hagas cambios en tu código local:

1. Ve a **"Files"** en PythonAnywhere
2. Click en `news_bot.py`
3. Click en **"Upload a file"** y selecciona el nuevo archivo
4. Confirma que quieres reemplazarlo
5. ✅ Los cambios se aplicarán en la próxima ejecución

---

## ❓ ¿Necesitas Ayuda?

Si algo no funciona:
1. Revisa los logs: `cat ~/telegram_bot/bot.log`
2. Verifica las tareas en el Dashboard
3. Asegúrate que los tokens en `.env` sean correctos
