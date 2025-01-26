from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets

from .models import CustomUser
from .responses import organization_created_response
from .serializers import CustomUserGetSerializer, ProfileUpdateSerializer, LoginSerializer, OrganizationCreateSerializer, \
    OrganizationSerializer, CustomUserSerializer, AddOrganizationSerializer, \
    OrganizationWithUsersSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view



from .services import create_organization, register_custom_user, authenticate_user, add_organizations_to_user, \
    get_all_organizations, update_user_profile, get_users_and_organizations_by_email, \
    get_organizations_for_user, get_all_organizations_with_users

@api_view(['POST'])
def register(request):
    custom_user = register_custom_user(request.data)
    return Response({
        'message': 'Пользователь успешно создан.',
        'user_id': custom_user.id,
    }, status=status.HTTP_201_CREATED)


@extend_schema(request=LoginSerializer)
@api_view(['POST'])
def login(request):
    tokens = authenticate_user(request.data)
    return Response(tokens, status=status.HTTP_200_OK)


class CustomUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        custom_user = CustomUserGetSerializer(request.user)
        return Response(custom_user.data, status=status.HTTP_200_OK)

    def patch(self, request):
        result = update_user_profile(request.user, request.data, ProfileUpdateSerializer)
        if result["success"]:
            return Response({"message": result["data"]}, status=status.HTTP_200_OK)
        return Response({"error": result["errors"]}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        organization = create_organization(request.data, OrganizationCreateSerializer)
        return organization_created_response(organization)


class AddOrganizationsToUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Валидируем данные
        serializer = AddOrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Добавляем организации через сервис
        organization_ids = serializer.validated_data['organization_ids']
        result = add_organizations_to_user(user_id, organization_ids)

        # Возвращаем успешный или ошибочный ответ
        if result["success"]:
            return Response({"message": result["message"]}, status=status.HTTP_200_OK)
        return Response({"error": result["message"]}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationListView(APIView):
    """Получение всех организаций"""

    def get(self, request, *args, **kwargs):
        # Получаем все организации через сервис
        organizations = get_all_organizations()

        # Сериализуем данные
        serializer = OrganizationSerializer(organizations, many=True)

        # Возвращаем успешный ответ
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)

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
