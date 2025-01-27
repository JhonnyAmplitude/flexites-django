FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Копируем скрипт entrypoint
COPY entrypoint.sh /app/

# Делаем скрипт исполняемым
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# Указываем entrypoint
ENTRYPOINT ["sh", "/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
