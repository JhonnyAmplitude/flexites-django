from .models import Organization, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


def register_user(data, serializer_class):
    """Регистрация пользователя через сериализатор."""
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

def authenticate_user(data, serializer_class):
    """
    Аутентификация пользователя через сериализатор.
    Возвращает пользователя и токены.
    """
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    return {
        "user": user,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

def create_organization(data, serializer_class):
    """Создает организацию через сериализатор."""
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

def add_organizations_to_user(user_id, organization_ids):
    """
    Добавляет указанные организации пользователю, если они ещё не добавлены.
    Возвращает сообщение об успехе или ошибке.
    """
    # Получаем пользователя или выбрасываем 404
    user = get_object_or_404(CustomUser, id=user_id)

    # Фильтруем организации по переданным ID
    organizations = Organization.objects.filter(id__in=organization_ids)
    existing_orgs = user.organizations.all()

    # Определяем новые организации
    new_orgs = [org for org in organizations if org not in existing_orgs]

    if not new_orgs:
        return {"success": False, "message": "Все указанные организации уже добавлены к этому пользователю"}

    # Добавляем новые организации
    user.organizations.add(*new_orgs)
    return {"success": True, "message": "Организации успешно добавлены"}

def get_all_organizations():
    """Получает все организации."""
    return Organization.objects.all()

def get_user_profile(user):
    """Возвращает профиль текущего пользователя."""
    return user

def update_user_profile(user, data, serializer_class):
    """Обновляет профиль пользователя."""
    serializer = serializer_class(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return {"success": True, "data": serializer.data}
    return {"success": False, "errors": serializer.errors}

def get_users_and_organizations_by_email(email):
    """Получает пользователей по email и его организации."""
    user = get_object_or_404(CustomUser, email=email)
    organizations = user.organizations.all()
    return user, organizations

def get_organizations_for_user(user_id):
    """Получает все организации для конкретного пользователя по его ID."""
    user = get_object_or_404(CustomUser, id=user_id)
    return user.organizations.all()

def get_all_organizations_with_users():
    """Получает все организации с прикрепленными пользователями."""
    return Organization.objects.all().prefetch_related('users')