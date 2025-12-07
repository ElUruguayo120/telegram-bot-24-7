# 📱 GUÍA PASO A PASO: Añadir Bot al Canal de Telegram

## ⚠️ PROBLEMA ACTUAL
El bot `@Conectordenotocias_bot` **NO está añadido** al canal `Portal`.

Error: `Forbidden: bot is not a member of the channel chat`

---

## ✅ SOLUCIÓN - Telegram Móvil (iOS/Android)

### Paso 1: Abre tu canal
1. Abre la app de Telegram
2. Ve a tu canal "Portal"

### Paso 2: Accede a la configuración
1. **Toca el nombre del canal** en la parte superior
2. Verás la información del canal

### Paso 3: Ve a Administradores
1. Busca la sección **"Administradores"** o **"Administrators"**
2. Tócala para ver la lista actual

### Paso 4: Añade el bot
1. Toca el botón **"Añadir Administrador"** (generalmente un ícono de +)
2. En el buscador, escribe: `Conectordenotocias_bot` (sin @)
3. Cuando aparezca el bot, **tócalo para seleccionarlo**

### Paso 5: Configura permisos
1. Verás una lista de permisos
2. **IMPORTANTE**: Activa SOLO este permiso:
   - ✅ **"Publicar mensajes"** o **"Post messages"**
3. Los demás permisos pueden estar desactivados

### Paso 6: Guarda
1. Toca **"Guardar"** o el ícono de ✓
2. El bot ahora debería aparecer en la lista de administradores

---

## ✅ SOLUCIÓN - Telegram Escritorio (Windows/Mac/Linux)

### Paso 1: Abre tu canal
1. Abre Telegram Desktop
2. Ve a tu canal "Portal" en la lista de chats

### Paso 2: Accede a la configuración
1. **Haz clic en el nombre del canal** en la parte superior
2. O haz clic en los **3 puntos** (⋮) → **"Gestionar canal"**

### Paso 3: Ve a Administradores
1. En el menú lateral, busca **"Administradores"**
2. Haz clic para ver la lista

### Paso 4: Añade el bot
1. Haz clic en **"Añadir Administrador"**
2. En el buscador, escribe: `Conectordenotocias_bot`
3. Haz clic en el bot cuando aparezca

### Paso 5: Configura permisos
1. Verás una ventana con permisos
2. **IMPORTANTE**: Marca SOLO:
   - ✅ **"Post messages"** (Publicar mensajes)
3. Desmarca todo lo demás si quieres

### Paso 6: Confirma
1. Haz clic en **"Save"** o **"Guardar"**
2. El bot aparecerá en la lista de administradores

---

## 🔍 VERIFICACIÓN

Después de añadir el bot, ejecuta este comando para verificar:

```bash
.venv/bin/python telegram_tech_news/full_diagnostic.py
```

Si todo está bien, verás:
- ✅ El bot en la lista de administradores
- ✅ "Puede publicar mensajes: SÍ"
- ✅ Mensaje de prueba enviado exitosamente

---

## ❓ PROBLEMAS COMUNES

### "No encuentro el bot al buscarlo"
- Asegúrate de escribir exactamente: `Conectordenotocias_bot`
- Intenta sin el @
- El bot debe aparecer con un ícono de bot 🤖

### "El bot aparece pero no puedo añadirlo"
- Asegúrate de que eres el **creador/administrador** del canal
- Solo los administradores con permisos pueden añadir otros administradores

### "Añadí el bot pero sigue sin funcionar"
- Verifica que el permiso **"Publicar mensajes"** esté ACTIVADO
- Espera 10-20 segundos y vuelve a intentar
- Cierra y vuelve a abrir Telegram

---

## 📞 SIGUIENTE PASO

Una vez que hayas añadido el bot correctamente, avísame y ejecutaremos la prueba final para confirmar que todo funciona! 🚀
