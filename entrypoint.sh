#!/bin/sh

# Прекращаем выполнение скрипта при ошибке
set -e

echo "Applying migrations..."
python manage.py migrate || echo "Migration failed"

echo "Starting development server..."
python manage.py runserver 0.0.0.0:8000
