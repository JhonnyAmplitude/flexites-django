from .models import Organization, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer, LoginSerializer, CustomUserPatchSerializer, CustomUserPostOrganizationsSerializer


def register_custom_user(request_data):
    serializer = RegistrationSerializer(data=request_data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

def authenticate_user(request_data):
    serializer = LoginSerializer(data=request_data)
    serializer.is_valid(raise_exception=True)
    refresh = RefreshToken.for_user(serializer.validated_data)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

def update_user_profile(custom_user, request_data):
    serializer = CustomUserPatchSerializer(custom_user, data=request_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

def get_user_by_id(user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return user

def create_organization(data, serializer_class):
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

def add_organizations_to_user(user_id, organization_ids):
    custom_user = get_object_or_404(CustomUser, id=user_id)

    # Фильтруем организации по переданным ID
    organizations = Organization.objects.filter(id__in=organization_ids)
    existing_orgs = custom_user.organizations.all()

    # Определяем новые организации
    new_orgs = [org for org in organizations if org not in existing_orgs]
    custom_user.organizations.add(*new_orgs)

    return custom_user

def get_all_organizations():
    return Organization.objects.all()

def get_all_organizations_with_users():
    return Organization.objects.all().prefetch_related('users')