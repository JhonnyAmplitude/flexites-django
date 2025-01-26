from rest_framework import serializers
from .models import CustomUser, Organization
from django.contrib.auth import authenticate
from .utils import process_avatar


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
        }


    def create(self, data):
        avatar_data = data.pop('avatar', None)
        avatar = process_avatar(avatar_data) if avatar_data else None
        return CustomUser.objects.create_user(**data, avatar=avatar)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email и пароль обязательны.")

        custom_user = authenticate(email=email, password=password)
        if not custom_user:
            raise serializers.ValidationError("Неверные учетные данные.")
        if not custom_user.is_active:
            raise serializers.ValidationError("Этот аккаунт деактивирован.")

        return custom_user


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'short_description']


class CustomUserSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone', 'avatar', 'organizations']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        custom_user = CustomUser.objects.create_user(**data)
        return custom_user

    def update(self, custom_user, data):
        if 'password' in data:
            password = data.pop('password')
            custom_user.set_password(password)
        return super().update(custom_user, data)


class CustomUserGetSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'first_name', 'last_name', 'avatar', 'organizations']


class CustomUserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'email': {'read_only': True},  # Email нельзя редактировать
        }

    def update(self, custom_user, data):
        if "avatar" in data:
            avatar = data["avatar"]
            data["avatar"] = process_avatar(avatar) if avatar else None

        return super().update(custom_user, data)

class CustomUserPostOrganizationsSerializer(serializers.Serializer):
    organization_ids = serializers.ListField(child=serializers.IntegerField())

    def validate_organization_ids(self, organization_ids):
        error = ''

        for id in organization_ids:
            try:
                Organization.objects.get(id=id)
            except Organization.DoesNotExist:
                error += f", {str(id)}" if error else f"{str(id)}"

        if error:
            raise serializers.ValidationError(f'Организации с ID "{error}" не существуют')

        return organization_ids


class CustomUserWithoutOrganizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'avatar']


class OrganizationWithUsersSerializer(serializers.ModelSerializer):
    users = CustomUserWithoutOrganizationsSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'short_description', 'users']