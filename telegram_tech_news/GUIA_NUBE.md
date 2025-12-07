# 🌐 Guía: Ejecutar el Bot 24/7 en la Nube

## ⚠️ IMPORTANTE: Limitación del Mac

**Python NO puede ejecutarse si tu Mac está completamente apagado.**

Para que el bot funcione 24/7 incluso con el ordenador apagado, necesitas un **servidor en la nube (VPS)**.

---

## 🆓 Opción 1: Servidor Gratuito (Recomendado para empezar)

### PythonAnywhere (Gratis)

**Ventajas:**
- ✅ Completamente gratis
- ✅ No necesitas tarjeta de crédito
- ✅ Fácil de configurar
- ✅ Perfecto para bots de Telegram

**Limitaciones:**
- ⏰ El bot se ejecutará cada hora (perfecto para tu caso)
- 🌐 No tiene acceso a internet directo (pero funciona para Telegram)

**Pasos:**

1. **Regístrate en PythonAnywhere**
   - Ve a: https://www.pythonanywhere.com
   - Crea una cuenta gratuita

2. **Sube tu código**
   - En "Files", crea una carpeta `telegram_bot`
   - Sube `news_bot.py` y `requirements.txt`

3. **Instala dependencias**
   - Ve a "Consoles" → "Bash"
   - Ejecuta:
     ```bash
     pip3 install --user feedparser requests
     ```

4. **Configura tarea programada**
   - Ve a "Tasks"
   - Añade una nueva tarea:
     ```bash
     python3 /home/tu_usuario/telegram_bot/news_bot.py
     ```
   - Configura para que se ejecute cada hora

---

## 💰 Opción 2: VPS de Pago (Más potente)

### DigitalOcean, AWS, o Google Cloud

**Costo:** ~$5-10/mes

**Ventajas:**
- ✅ Control total
- ✅ Funciona 24/7 sin restricciones
- ✅ Puedes ejecutar múltiples bots

### Pasos Rápidos (DigitalOcean):

1. **Crear Droplet**
   - Regístrate en DigitalOcean
   - Crea un Droplet Ubuntu ($6/mes)
   - Obtén la IP del servidor

2. **Conectar por SSH**
   ```bash
   ssh root@tu_ip_del_servidor
   ```

3. **Instalar Python y dependencias**
   ```bash
   apt update
   apt install python3 python3-pip -y
   pip3 install feedparser requests
   ```

4. **Subir tu código**
   Desde tu Mac:
   ```bash
   scp -r telegram_tech_news root@tu_ip:/root/
   ```

5. **Ejecutar el bot**
   En el servidor:
   ```bash
   cd /root/telegram_tech_news
   nohup python3 news_bot.py &
   ```

6. **Hacer que se inicie automáticamente**
   ```bash
   # Crear servicio systemd
   nano /etc/systemd/system/telegram-bot.service
   ```
   
   Pega esto:
   ```ini
   [Unit]
   Description=Telegram Tech News Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/telegram_tech_news
   ExecStart=/usr/bin/python3 /root/telegram_tech_news/news_bot.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
   
   Luego:
   ```bash
   systemctl enable telegram-bot
   systemctl start telegram-bot
   systemctl status telegram-bot
   ```

---

## 🏠 Opción 3: Mantener tu Mac encendido

Si prefieres no usar la nube:

1. **Evitar que el Mac se duerma**
   - Ve a Preferencias del Sistema → Batería/Energía
   - Desactiva "Suspender automáticamente"
   - O usa: `caffeinate -s` en terminal

2. **Ejecutar el bot como servicio**
   ```bash
   cd telegram_tech_news
   ./setup.sh
   ```
   Elige opción 2

**Nota:** El Mac debe estar encendido (puede tener la pantalla apagada)

---

## 📊 Comparación

| Opción | Costo | Dificultad | Funciona con Mac apagado |
|--------|-------|------------|--------------------------|
| PythonAnywhere | Gratis | Fácil | ✅ Sí |
| VPS (DigitalOcean) | $6/mes | Media | ✅ Sí |
| Mac encendido | Gratis | Fácil | ❌ No |

---

## 🎯 Recomendación

Para empezar: **PythonAnywhere** (gratis y fácil)

Si quieres más control: **DigitalOcean** ($6/mes)

---

## ❓ ¿Necesitas ayuda?

Si eliges alguna opción de la nube, puedo guiarte paso a paso en la configuración.
