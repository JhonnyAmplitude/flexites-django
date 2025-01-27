FROM python:3.11-slim

# Установка зависимостей для работы с Python
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование проекта
COPY . /app

# Установка прав на запись для базы данных SQLite
RUN chmod -R 777 /app

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Команда по умолчанию для выполнения миграции и запуска сервера
CMD ["sh", "-c", "python manage.py migrate || echo 'Migration failed' && python manage.py runserver 0.0.0.0:8000"]
