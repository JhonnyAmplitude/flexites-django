from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets

from .models import CustomUser
from .responses import organization_created_response, registration_successful_response, login_successful_response, \
    success_response, error_response
from .serializers import RegistrationSerializer, LoginSerializer, ProfileUpdateSerializer, OrganizationCreateSerializer, \
    OrganizationSerializer, CustomUserSerializer, AddOrganizationSerializer, \
    OrganizationWithUsersSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


from .services import create_organization, register_custom_user, authenticate_user, add_organizations_to_user, \
    get_all_organizations, get_user_profile, update_user_profile, get_users_and_organizations_by_email, \
    get_organizations_for_user, get_all_organizations_with_users


class RegistrationView(APIView):
    def post(self, request):
        custom_user = register_custom_user(request.data)
        return registration_successful_response(custom_user)


class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: LoginSerializer,
            400: 'Некорректные данные для логина',
        }
    )
    def post(self, request, *args, **kwargs):
        tokens = authenticate_user(request.data, LoginSerializer)
        return login_successful_response(tokens)


class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        organization = create_organization(request.data, OrganizationCreateSerializer)
        return organization_created_response(organization)


class AddOrganizationsToUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Валидируем данные
        serializer = AddOrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Добавляем организации через сервис
        organization_ids = serializer.validated_data['organization_ids']
        result = add_organizations_to_user(user_id, organization_ids)

        # Возвращаем успешный или ошибочный ответ
        if result["success"]:
            return success_response(result["message"])
        return error_response(result["message"])


class OrganizationListView(APIView):
    """Получение всех организаций"""

    def get(self, request, *args, **kwargs):
        # Получаем все организации через сервис
        organizations = get_all_organizations()

        # Сериализуем данные
        serializer = OrganizationSerializer(organizations, many=True)

        # Возвращаем успешный ответ
        return success_response(serializer.data)


class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Получение текущего профиля."""
        user_profile = get_user_profile(request.user)
        serializer = ProfileUpdateSerializer(user_profile)
        return success_response(serializer.data)

    def patch(self, request):
        """Обновление профиля."""
        result = update_user_profile(request.user, request.data, ProfileUpdateSerializer)
        if result["success"]:
            return success_response(result["data"])
        return error_response(result["errors"])

class GetUsersAndTheirOrganizationsViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().prefetch_related('organizations')
    serializer_class = CustomUserSerializer

    def get(self, request, email):
        """Получение пользователя и его организаций по email."""
        user, organizations = get_users_and_organizations_by_email(email)

        # Сериализуем организации
        serializer = OrganizationSerializer(organizations, many=True)

        return Response(serializer.data)


class UserOrganizationsView(APIView):
    """Получение организаций конкретного пользователя по ID."""

    def get(self, request, user_id):
        """Получение организаций для пользователя по его ID."""
        organizations = get_organizations_for_user(user_id)

        # Сериализуем данные
        serializer = OrganizationSerializer(organizations, many=True)

        return Response(serializer.data)


class GetAllOrganizationsWithUsersView(APIView):
    """Получение всех организаций с прикрепленными пользователями."""

    def get(self, request):
        """Получение списка всех организаций с пользователями."""
        organizations = get_all_organizations_with_users()

        # Сериализуем организации с пользователями
        serializer = OrganizationWithUsersSerializer(organizations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
