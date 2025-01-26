from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models import CustomUser, Organization
from .responses import organization_created_response
from .serializers import CustomUserGetSerializer, LoginSerializer, \
    OrganizationSerializer, CustomUserSerializer, CustomUserPostOrganizationsSerializer, \
    OrganizationWithUsersSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view

from .services import create_organization, register_custom_user, authenticate_user, add_organizations_to_user, \
    update_user_profile, \
    get_user_by_id

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
        serializer = CustomUserGetSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        updated_custom_user = update_user_profile(request.user, request.data)
        return Response(updated_custom_user, status=status.HTTP_200_OK)


class CustomUserByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _, user_id):
        user = get_user_by_id(user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def post(self, request, user_id):
        serializer = CustomUserPostOrganizationsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization_ids = serializer.validated_data['organization_ids']

        custom_user = add_organizations_to_user(user_id, organization_ids)

        serializer = CustomUserGetSerializer(custom_user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all().prefetch_related('organizations')
    serializer_class = CustomUserSerializer


class OrganizationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class OrganizationsWithUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Organization.objects.all().prefetch_related("users")
    serializer_class = OrganizationWithUsersSerializer

class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        organization = create_organization(request.data, OrganizationSerializer)
        return organization_created_response(organization)