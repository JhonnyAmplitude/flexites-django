FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

