# ⏰ Función de Alarma en Telegram - Cuenta Regresiva en Tiempo Real

## 🎉 Nueva Funcionalidad Agregada

El bot ahora incluye un **sistema de alarmas con cuenta regresiva en tiempo real** que actualiza el mensaje cada segundo dentro de Telegram.

---

## 🚀 Cómo Usar

### Comando Básico
```
/alarma [tiempo]
```

### 📋 Formatos Soportados

#### 1. **Solo Minutos** (por defecto)
```
/alarma 5       → Alarma de 5 minutos
/alarma 10      → Alarma de 10 minutos
/alarma 30      → Alarma de 30 minutos
```

#### 2. **Horas** (con sufijo `h`)
```
/alarma 1h      → Alarma de 1 hora
/alarma 2h      → Alarma de 2 horas
/alarma 24h     → Alarma de 24 horas
```

#### 3. **Minutos y Segundos** (con sufijos `m` y `s`)
```
/alarma 1m 30s  → Alarma de 1 minuto y 30 segundos
/alarma 0m 10s  → Alarma de 10 segundos
/alarma 5m 0s   → Alarma de 5 minutos exactos
```

#### 4. **Combinaciones**
```
/alarma 1h 30m      → Alarma de 1 hora y 30 minutos
/alarma 2h 15m 30s  → Alarma de 2:15:30
```

---

## 🎬 Funcionamiento

### 1. **Configuración Inicial**
Cuando envías el comando, el bot responde:
```
⏰ Alarma configurada

⏱️ Tiempo: 00:05:00

🔔 Te avisaré cuando termine
```

### 2. **Cuenta Regresiva en Tiempo Real**
El mensaje se actualiza **cada segundo** mostrando:
```
⏰ Cuenta Regresiva

⏱️ 00:04:59

⏳ Tiempo restante...
```

Los números cambian automáticamente:
- `00:04:59`
- `00:04:58`
- `00:04:57`
- ...
- `00:00:03`
- `00:00:02`
- `00:00:01`

### 3. **Alarma Finalizada**
Cuando llega a cero, el mensaje cambia a:
```
🔔 ¡ALARMA! 🔔

⏰ El tiempo ha terminado

✅ Alarma de 00:05:00 completada
```

---

## ✨ Características

### ✅ Actualización en Tiempo Real
- El mensaje se edita cada segundo
- No envía mensajes nuevos (solo actualiza el existente)
- Formato de reloj digital: `HH:MM:SS`

### ✅ Threading Asíncrono
- Usa threads para no bloquear el bot
- Múltiples alarmas simultáneas soportadas
- No interfiere con otras funciones del bot

### ✅ Formato Flexible
- Acepta horas, minutos y segundos
- Combinaciones libres
- Valores por defecto inteligentes

### ✅ Validación de Errores
- Detecta tiempos inválidos
- Muestra mensajes de ayuda
- Manejo robusto de excepciones

---

## 📱 Ejemplos de Uso

### Ejemplo 1: Alarma Rápida (10 segundos)
```
Tú: /alarma 0m 10s

Bot: ⏰ Alarma configurada
     ⏱️ Tiempo: 00:00:10
     🔔 Te avisaré cuando termine

[Actualización cada segundo]
Bot: ⏰ Cuenta Regresiva
     ⏱️ 00:00:09
     ⏳ Tiempo restante...

[Continúa hasta...]
Bot: 🔔 ¡ALARMA! 🔔
     ⏰ El tiempo ha terminado
     ✅ Alarma de 00:00:10 completada
```

### Ejemplo 2: Alarma de Cocina (5 minutos)
```
Tú: /alarma 5

Bot: ⏰ Alarma configurada
     ⏱️ Tiempo: 00:05:00
     🔔 Te avisaré cuando termine

[Cuenta regresiva en tiempo real]
Bot: ⏰ Cuenta Regresiva
     ⏱️ 00:04:59
     ⏳ Tiempo restante...
```

### Ejemplo 3: Alarma de Estudio (25 minutos - Pomodoro)
```
Tú: /alarma 25

Bot: ⏰ Alarma configurada
     ⏱️ Tiempo: 00:25:00
     🔔 Te avisaré cuando termine
```

### Ejemplo 4: Alarma Larga (2 horas)
```
Tú: /alarma 2h

Bot: ⏰ Alarma configurada
     ⏱️ Tiempo: 02:00:00
     🔔 Te avisaré cuando termine
```

---

## 🛠️ Detalles Técnicos

### Implementación
- **Threading:** Usa `threading.Thread` para ejecución asíncrona
- **Actualización:** `editMessageText` de Telegram API
- **Precisión:** Actualización cada 1 segundo
- **Formato:** Función `format_time()` para HH:MM:SS

### Código Clave
```python
def format_time(seconds):
    """Format seconds to HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
```

### Thread de Cuenta Regresiva
```python
def countdown_thread():
    remaining = total_seconds
    last_update = time.time()
    
    while remaining > 0:
        current_time = time.time()
        if current_time - last_update >= 1:
            remaining -= 1
            last_update = current_time
            
            # Actualizar mensaje cada segundo
            countdown_msg = f"⏰ Cuenta Regresiva\n\n⏱️ {format_time(remaining)}\n\n⏳ Tiempo restante..."
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText", ...)
        
        time.sleep(0.1)
```

---

## 🎯 Casos de Uso

### 🍳 Cocina
```
/alarma 15      → Pasta (15 min)
/alarma 3       → Huevos duros (3 min)
/alarma 45      → Pizza (45 min)
```

### 📚 Estudio (Técnica Pomodoro)
```
/alarma 25      → Sesión de estudio
/alarma 5       → Descanso corto
/alarma 15      → Descanso largo
```

### 💪 Ejercicio
```
/alarma 1m      → Plancha
/alarma 30s     → Descanso entre series
/alarma 20      → Cardio
```

### ☕ Recordatorios
```
/alarma 10      → Café listo
/alarma 1h      → Reunión en 1 hora
/alarma 30      → Salir de casa
```

---

## 📊 Comparación con Otras Soluciones

| Característica | Este Bot | Alarmas Normales |
|----------------|----------|------------------|
| Actualización en tiempo real | ✅ Cada segundo | ❌ Solo al final |
| Múltiples alarmas | ✅ Sí | ⚠️ Limitado |
| Formato flexible | ✅ h/m/s | ⚠️ Fijo |
| Dentro de Telegram | ✅ Sí | ❌ App separada |
| Sin notificaciones spam | ✅ Edita mensaje | ❌ Múltiples mensajes |

---

## 🔔 Comandos Relacionados

### Ver Ayuda de Alarma
```
/alarma
```
Muestra el mensaje de ayuda con ejemplos.

### Actualizar Menú Principal
```
/start
```
Ahora incluye `/alarma` en la lista de comandos.

---

## 💡 Tips y Trucos

### 1. **Alarmas Múltiples**
Puedes configurar varias alarmas simultáneamente:
```
/alarma 5       → Primera alarma
/alarma 10      → Segunda alarma
/alarma 15      → Tercera alarma
```

### 2. **Alarmas Cortas para Pruebas**
```
/alarma 0m 5s   → Prueba rápida de 5 segundos
```

### 3. **Formato Mixto**
```
/alarma 1h 30m 45s   → Máxima precisión
```

### 4. **Valores por Defecto**
Si no especificas sufijo, asume minutos:
```
/alarma 20 = /alarma 20m
```

---

## 🚨 Limitaciones

### Telegram API
- Telegram tiene límites de edición de mensajes
- Máximo ~30 ediciones por minuto por mensaje
- Para alarmas muy largas, considera reducir frecuencia de actualización

### Precisión
- Precisión de ~1 segundo
- Puede variar ligeramente por latencia de red
- Suficiente para uso cotidiano

---

## 🎨 Personalización Futura

### Ideas para Mejorar
1. **Sonidos personalizados** (si Telegram lo soporta)
2. **Alarmas recurrentes** (diarias, semanales)
3. **Etiquetas** para identificar alarmas
4. **Pausar/Reanudar** alarmas en curso
5. **Lista de alarmas activas** con `/alarmas`

---

## 📝 Resumen

✅ **Comando:** `/alarma [tiempo]`  
✅ **Actualización:** Cada segundo en tiempo real  
✅ **Formato:** HH:MM:SS  
✅ **Notificación:** Mensaje editado, no spam  
✅ **Flexible:** Horas, minutos, segundos  
✅ **Múltiple:** Varias alarmas simultáneas  

---

**¡Prueba la alarma ahora mismo!**

Envía al bot: `/alarma 0m 10s` para una demostración rápida de 10 segundos.

---

*Última actualización: 2025-12-06 22:20*  
*Versión: 2.1 - Con sistema de alarmas en tiempo real*
