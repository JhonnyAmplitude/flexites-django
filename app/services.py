from .models import Organization, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer, LoginSerializer


def register_custom_user(request_data) -> CustomUser:
    custom_user = RegistrationSerializer(data=request_data)
    custom_user.is_valid(raise_exception=True)
    return custom_user.save()

def authenticate_user(request_data):
    custom_user = LoginSerializer(data=request_data)
    custom_user.is_valid(raise_exception=True)
    refresh = RefreshToken.for_user(custom_user.validated_data)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

def create_organization(data, serializer_class):
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

def add_organizations_to_user(user_id, organization_ids):
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
    return Organization.objects.all()

def update_user_profile(user, data, serializer_class):
    serializer = serializer_class(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return {"success": True, "data": serializer.data}
    return {"success": False, "errors": serializer.errors}

def get_users_and_organizations_by_email(email):
    user = get_object_or_404(CustomUser, email=email)
    organizations = user.organizations.all()
    return user, organizations

def get_organizations_for_user(user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return user.organizations.all()

def get_all_organizations_with_users():
    return Organization.objects.all().prefetch_related('users')