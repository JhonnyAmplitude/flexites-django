from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from .settings import AVATARS_PATH


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.update({'is_staff': True, 'is_superuser': True})
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,12}$',
                message="Номер телефона должен быть в формате: '+999999999'. До 12 цифр."
            )
        ],
    )
    avatar = models.ImageField(
        upload_to=f'${AVATARS_PATH}/',
        blank=True,
        null=True,
    )
    organizations = models.ManyToManyField(
        'Organization',
        related_name='users',
        blank=True,
        verbose_name="Организации"
    )
    username = None  # Исключаем username из модели
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    short_description = models.TextField(blank=True, null=True, verbose_name="Краткое описание")

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name

