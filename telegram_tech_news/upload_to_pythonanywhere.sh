#!/bin/bash

# Script para subir archivos a PythonAnywhere
# Uso: ./upload_to_pythonanywhere.sh

echo "🚀 Subiendo archivos a PythonAnywhere..."
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Solicitar credenciales de PythonAnywhere
echo -e "${YELLOW}Ingresa tu nombre de usuario de PythonAnywhere:${NC}"
read -p "Usuario: " PA_USERNAME

echo ""
echo -e "${YELLOW}Ingresa tu contraseña de PythonAnywhere:${NC}"
read -sp "Contraseña: " PA_PASSWORD
echo ""
echo ""

# Servidor de PythonAnywhere
PA_SERVER="ssh.pythonanywhere.com"

# Archivos a subir
FILES=(
    "news_bot.py"
    "requirements.txt"
    ".env"
    "posted_articles.json"
)

echo -e "${GREEN}📂 Archivos a subir:${NC}"
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file (no existe, se omitirá)"
    fi
done
echo ""

# Confirmar
echo -e "${YELLOW}¿Continuar con la subida? (s/n)${NC}"
read -p "> " CONFIRM

if [ "$CONFIRM" != "s" ] && [ "$CONFIRM" != "S" ]; then
    echo -e "${RED}❌ Cancelado${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}📤 Subiendo archivos...${NC}"

# Usar sshpass si está disponible, sino usar scp normal
if command -v sshpass &> /dev/null; then
    # Con sshpass (automático)
    for file in "${FILES[@]}"; do
        if [ -f "$file" ]; then
            echo "  Subiendo $file..."
            sshpass -p "$PA_PASSWORD" scp "$file" "$PA_USERNAME@$PA_SERVER:~/telegram_bot/"
            if [ $? -eq 0 ]; then
                echo -e "  ${GREEN}✅ $file subido${NC}"
            else
                echo -e "  ${RED}❌ Error subiendo $file${NC}"
            fi
        fi
    done
else
    # Sin sshpass (manual)
    echo -e "${YELLOW}⚠️  sshpass no está instalado. Tendrás que ingresar la contraseña para cada archivo.${NC}"
    echo ""
    for file in "${FILES[@]}"; do
        if [ -f "$file" ]; then
            echo "  Subiendo $file..."
            scp "$file" "$PA_USERNAME@$PA_SERVER:~/telegram_bot/"
            if [ $? -eq 0 ]; then
                echo -e "  ${GREEN}✅ $file subido${NC}"
            else
                echo -e "  ${RED}❌ Error subiendo $file${NC}"
            fi
        fi
    done
fi

echo ""
echo -e "${GREEN}✅ ¡Proceso completado!${NC}"
echo ""
echo -e "${YELLOW}📝 Próximos pasos:${NC}"
echo "  1. Ve a https://www.pythonanywhere.com"
echo "  2. Verifica que los archivos estén en ~/telegram_bot/"
echo "  3. La tarea programada usará los nuevos archivos en la próxima ejecución"
echo ""
