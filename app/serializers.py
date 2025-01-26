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


    def create(self, data) -> CustomUser:
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


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'short_description']


class CustomUserGetSerializer(serializers.ModelSerializer):
    organizations = OrganizationCreateSerializer(many=True)

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

    def update(self, custom_user, data) -> CustomUser:
        if "avatar" in data:
            avatar = data["avatar"]
            data["avatar"] = process_avatar(avatar) if avatar else None

        return super().update(custom_user, data)

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'short_description']

class AddOrganizationSerializer(serializers.Serializer):
    organization_ids = serializers.ListField(child=serializers.IntegerField())

    def validate_organization_ids(self, value):
        for org_id in value:
            try:
                Organization.objects.get(id=org_id)
            except Organization.DoesNotExist:
                raise serializers.ValidationError(f"Организация с ID {org_id} не существует")
        return value


class CustomUserSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'organizations', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class OrganizationWithUsersSerializer(serializers.ModelSerializer):
    users = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'short_description', 'users']


class CustomUserListSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name', 'organizations']