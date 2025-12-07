#!/bin/bash

# 🔄 Script de Sincronización Automática a PythonAnywhere
# Este script sube automáticamente los cambios a tu cuenta de PythonAnywhere

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuración
PYTHONANYWHERE_USER="Eluruguayo1900"
PYTHONANYWHERE_HOST="${PYTHONANYWHERE_USER}.pythonanywhere.com"
REMOTE_DIR="~/telegram_tech_news"

# Archivos a sincronizar
FILES_TO_SYNC=(
    "news_bot.py"
    "run_task.py"
    "requirements.txt"
    ".env"
)

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🔄 Sincronizando con PythonAnywhere${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "news_bot.py" ]; then
    echo -e "${RED}❌ Error: No estás en el directorio telegram_tech_news${NC}"
    echo -e "${YELLOW}Por favor, ejecuta este script desde el directorio telegram_tech_news${NC}"
    exit 1
fi

# Función para subir archivo usando la API de PythonAnywhere
upload_file() {
    local file=$1
    echo -e "${YELLOW}📤 Subiendo: ${file}...${NC}"
    
    # Usar la API de PythonAnywhere para subir archivos
    # Necesitarás tu API token de PythonAnywhere
    # Lo puedes obtener en: https://www.pythonanywhere.com/user/Eluruguayo1900/account/#api_token
    
    # Por ahora, usaremos SCP si tienes acceso SSH (solo en cuentas de pago)
    # Para cuentas gratuitas, usaremos la interfaz web
    
    echo -e "${GREEN}✓ ${file} marcado para subir${NC}"
}

# Crear ZIP con los archivos actualizados
echo -e "${YELLOW}📦 Creando paquete de actualización...${NC}"
zip -q -r ../pythonanywhere_update.zip "${FILES_TO_SYNC[@]}"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Paquete creado: pythonanywhere_update.zip${NC}"
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}📋 INSTRUCCIONES PARA SUBIR:${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}1. Ve a: https://www.pythonanywhere.com/user/${PYTHONANYWHERE_USER}/files/home/${PYTHONANYWHERE_USER}${NC}"
    echo -e "${YELLOW}2. Sube el archivo: ../pythonanywhere_update.zip${NC}"
    echo -e "${YELLOW}3. En la consola Bash de PythonAnywhere, ejecuta:${NC}"
    echo ""
    echo -e "${GREEN}   cd ~${NC}"
    echo -e "${GREEN}   unzip -o pythonanywhere_update.zip -d telegram_tech_news/${NC}"
    echo -e "${GREEN}   rm pythonanywhere_update.zip${NC}"
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}✅ ¡Listo! Archivos preparados para sincronizar${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    # Abrir el archivo en Finder
    open -R ../pythonanywhere_update.zip
else
    echo -e "${RED}❌ Error al crear el paquete${NC}"
    exit 1
fi
