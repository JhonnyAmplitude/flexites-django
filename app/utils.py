import os
import uuid
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .settings import AVATARS_PATH


def process_avatar(avatar):
    # Генерируем уникальное имя файла
    extension = avatar.name.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{extension}"

    # Открываем изображение
    img = Image.open(avatar)
    img.thumbnail((200, 200))

    # Сохраняем обработанное изображение
    temp_file = ContentFile(b'')
    img.save(temp_file, format=img.format)
    temp_file.seek(0)

    # Сохраняем файл
    file_path = os.path.join(AVATARS_PATH, filename)
    default_storage.save(file_path, temp_file)

    return filename
