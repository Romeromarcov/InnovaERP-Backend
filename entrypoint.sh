#!/bin/sh
set -e # Salir inmediatamente si un comando falla

# Variables para la conexión a la base de datos (se usan las del entorno)
DB_HOST="${DB_HOST:-db}" # Usa 'db' como valor por defecto si DB_HOST no está seteado
DB_PORT="${DB_PORT:-5432}" # Usa '5432' como valor por defecto si DB_PORT no está seteado

echo "Waiting for postgres at ${DB_HOST}:${DB_PORT}..."
# Espera activa por la base de datos usando netcat (nc)
while ! nc -z ${DB_HOST} ${DB_PORT}; do
  sleep 0.1 # Espera un poco antes de reintentar
done
echo "PostgreSQL started"

# Generar migraciones (para cualquier cambio en modelos)
echo "Generating database migrations..."
python manage.py makemigrations --noinput

# Aplicar migraciones de la base de datos
# 'migrate' también se encarga de 'makemigrations' en muchos casos o las aplica si ya existen
echo "Applying database migrations..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Ejecutar el comando principal que se le pasó al contenedor (e.g., runserver)
echo "Executing main command: $@"
exec "$@" # ¡Esta es la clave! Ejecuta el comando pasado y lo mantiene vivo.