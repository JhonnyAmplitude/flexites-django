## Установка

1. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Выполнить миграции:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Запустить сервер:
   ```bash
   python manage.py runserver
   
### Версия API

Все запросы к API начинаются с `/api/v1/`.

Вся документация `/api/v1/docs/`.