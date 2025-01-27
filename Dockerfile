FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    python3-dev
# Указываем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ./app /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем и делаем скрипт entrypoint исполняемым
COPY ./app/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Указываем скрипт в качестве команды запуска контейнера
CMD ["/app/entrypoint.sh"]
