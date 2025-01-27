FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Выполнение миграций перед запуском приложения
RUN python manage.py migrate

# Запуск Django сервера (если используете runserver)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

