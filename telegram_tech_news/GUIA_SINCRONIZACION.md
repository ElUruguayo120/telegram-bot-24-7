# 🔄 Guía de Sincronización Automática con PythonAnywhere

## 📋 Resumen

Cada vez que modifiques el código localmente, puedes sincronizarlo automáticamente con PythonAnywhere usando uno de estos métodos:

---

## 🚀 Método 1: Script Python Automático (RECOMENDADO)

### Configuración Inicial (Solo una vez)

1. **Obtén tu API Token de PythonAnywhere:**
   - Ve a: https://www.pythonanywhere.com/user/Eluruguayo1900/account/#api_token
   - Copia tu API token (si no tienes uno, créalo haciendo clic en "Create a new API token")

2. **Ejecuta el script por primera vez:**
   ```bash
   cd telegram_tech_news
   python3 auto_sync.py
   ```

3. **Pega tu API token** cuando te lo pida
4. **Guarda el token** para futuras sincronizaciones (responde 's')

### Uso Diario

Cada vez que modifiques el código:

```bash
cd telegram_tech_news
python3 auto_sync.py
```

**¡Eso es todo!** El script subirá automáticamente todos los archivos modificados.

---

## 📦 Método 2: Script Shell Manual

Si prefieres un método más simple (sin API):

```bash
cd telegram_tech_news
./sync_to_pythonanywhere.sh
```

Esto creará un archivo `pythonanywhere_update.zip` que debes subir manualmente:

1. Ve a: https://www.pythonanywhere.com/user/Eluruguayo1900/files/home/Eluruguayo1900
2. Sube el archivo `pythonanywhere_update.zip`
3. En la consola Bash de PythonAnywhere:
   ```bash
   cd ~
   unzip -o pythonanywhere_update.zip -d telegram_tech_news/
   rm pythonanywhere_update.zip
   ```

---

## 🌐 Método 3: Interfaz Web de PythonAnywhere

### Subir archivos uno por uno:

1. **Ve a Files:** https://www.pythonanywhere.com/user/Eluruguayo1900/files/home/Eluruguayo1900/telegram_tech_news
2. **Click en el archivo** que quieres actualizar (ej: `news_bot.py`)
3. **Click en "Upload a file"**
4. **Selecciona el archivo** desde tu Mac
5. **Confirma** para sobrescribir

---

## 🔄 Método 4: Usando el Navegador (Automático)

Puedo automatizar la subida usando el navegador. Solo dime:

```
"Sube los cambios a PythonAnywhere"
```

Y yo me encargaré de:
1. Abrir PythonAnywhere en el navegador
2. Navegar a la sección de Files
3. Subir los archivos modificados automáticamente

---

## 📝 Archivos que se Sincronizan

Por defecto, estos archivos se sincronizan automáticamente:

- ✅ `news_bot.py` - Código principal del bot
- ✅ `run_task.py` - Script de ejecución programada
- ✅ `requirements.txt` - Dependencias
- ✅ `.env` - Variables de entorno (credenciales)

---

## 🎯 Workflow Recomendado

### Cuando modifiques el código:

1. **Edita** el archivo localmente (ej: `news_bot.py`)
2. **Prueba** los cambios localmente (opcional)
3. **Sincroniza** con PythonAnywhere:
   ```bash
   python3 auto_sync.py
   ```
4. **Verifica** en la próxima ejecución programada (cada hora)

---

## 🔍 Verificar que la Sincronización Funcionó

### Opción 1: Ver el archivo en PythonAnywhere
1. Ve a: https://www.pythonanywhere.com/user/Eluruguayo1900/files/home/Eluruguayo1900/telegram_tech_news
2. Click en el archivo (ej: `news_bot.py`)
3. Verifica que tenga tus cambios

### Opción 2: Ver los logs
1. Espera a la próxima ejecución programada (cada hora)
2. Ve a: https://www.pythonanywhere.com/user/Eluruguayo1900/files/home/Eluruguayo1900/telegram_tech_news/bot.log
3. Verifica que los logs reflejen tus cambios

---

## ⚡ Sincronización Instantánea

Si necesitas que los cambios se apliquen **inmediatamente** (sin esperar a la próxima hora):

1. **Sincroniza** los archivos (método 1, 2, 3 o 4)
2. **Ve a Tasks:** https://www.pythonanywhere.com/user/Eluruguayo1900/tasks_tab/
3. **Click en "Run now"** junto a tu tarea programada
4. **Espera 10 segundos** y verifica los logs

---

## 🛠️ Troubleshooting

### Error: "API token inválido"
- Verifica que copiaste el token completo
- Genera un nuevo token en: https://www.pythonanywhere.com/user/Eluruguayo1900/account/#api_token

### Error: "Archivo no encontrado"
- Asegúrate de ejecutar el script desde el directorio `telegram_tech_news`
- Verifica que el archivo existe localmente

### Los cambios no se reflejan
- Verifica que el archivo se subió correctamente
- Espera a la próxima ejecución programada (cada hora)
- O ejecuta manualmente con "Run now" en Tasks

---

## 💡 Tips

1. **Guarda el API token** la primera vez para no tener que ingresarlo siempre
2. **Usa `auto_sync.py`** para sincronización rápida y automática
3. **Verifica los logs** después de cada sincronización
4. **Haz backup** de `posted_articles.json` periódicamente

---

## 🎉 Ejemplo de Uso

```bash
# 1. Modificas news_bot.py localmente
nano news_bot.py

# 2. Sincronizas con PythonAnywhere
python3 auto_sync.py

# 3. ¡Listo! Los cambios se aplicarán en la próxima ejecución
```

---

## 📞 Comandos Rápidos

```bash
# Sincronizar con API (automático)
python3 auto_sync.py

# Crear ZIP para subir manualmente
./sync_to_pythonanywhere.sh

# Ver archivos locales
ls -lh

# Ver diferencias con versión anterior
git diff news_bot.py
```

---

**¿Prefieres que automatice completamente la sincronización?**

Puedo crear un watcher que detecte cambios automáticamente y los suba a PythonAnywhere sin que tengas que hacer nada. Solo dime si lo quieres! 😊
