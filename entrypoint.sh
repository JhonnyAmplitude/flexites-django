#!/bin/sh

# Выполняем миграции
python manage.py makemigrations
python manage.py migrate

# Запускаем сервер
exec "$@"
