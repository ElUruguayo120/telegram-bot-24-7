#!/bin/bash
echo "🚀 Iniciando proceso de subida a GitHub..."
echo ""
echo "Por favor, pega la URL de tu repositorio de GitHub (ej: https://github.com/usuario/repo.git):"
read REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Error: No has introducido ninguna URL."
    exit 1
fi

echo ""
echo "🔗 Conectando con $REPO_URL..."

# Remove existing remote if exists
git remote remove origin 2>/dev/null

# Add new remote
git remote add origin "$REPO_URL"

# Rename branch to main if needed
git branch -M main

# Push
echo "⬆️  Subiendo archivos..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Subida completada con éxito!"
    echo "Ahora ve a Railway.app y conecta este repositorio."
else
    echo ""
    echo "❌ Error al subir. Asegúrate de que el repositorio está vacío y tienes permisos."
fi
