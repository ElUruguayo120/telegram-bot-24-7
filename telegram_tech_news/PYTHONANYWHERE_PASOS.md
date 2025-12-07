# 📝 Pasos Rápidos: PythonAnywhere (Copy & Paste)

## ⚡ Guía Express (5 minutos)

### 1️⃣ Crear cuenta
https://www.pythonanywhere.com → "Sign up for free"

### 2️⃣ Subir archivos

**En el Dashboard:**
- "Files" → Crear carpeta `telegram_bot`
- Subir estos archivos:
  - ✅ `news_bot.py`
  - ✅ `run_task.py` (el nuevo script wrapper)
  - ✅ `requirements.txt`

### 3️⃣ Instalar dependencias

**Consola Bash:**
```bash
cd ~/telegram_bot
pip3.9 install --user feedparser requests google-generativeai beautifulsoup4
```

### 4️⃣ Configurar variables

**Crear archivo `.env` en `telegram_bot`:**
```
TELEGRAM_BOT_TOKEN=6665925860:AAHa-Eu8xKhece83HaKEsHTB8x8CGF61Czk
GEMINI_API_KEY=AIzaSyAYgke20w4fNeZL_zK3wm8r19NgbIat6s0
```

### 5️⃣ Probar

**Consola Bash:**
```bash
cd ~/telegram_bot
python3.9 run_task.py
```

(Debería ejecutarse y funcionar. Presiona Ctrl+C después de verificar)

### 6️⃣ Crear tarea programada

**Dashboard → "Tasks" → "Create a new scheduled task":**

**Command:**
```
cd ~/telegram_bot && python3.9 run_task.py
```

**Hour:** (dejar vacío)
**Minute:** `0`
**Enabled:** ✅

### 7️⃣ ¡Listo!

El bot se ejecutará **cada hora** automáticamente.

---

## 📋 Checklist

- [ ] Cuenta creada
- [ ] Archivos subidos
- [ ] Dependencias instaladas
- [ ] Variables configuradas (.env)
- [ ] Probado manualmente
- [ ] Tarea programada creada
- [ ] Bot funcionando

---

## 🔍 Verificar

**Ver logs:**
```bash
tail -20 ~/telegram_bot/bot.log
```

**Ver tareas:**
Dashboard → "Tasks" → Ver historial de ejecuciones

---

✅ **El bot funcionará cada hora, 24/7, incluso con tu Mac apagado!**

