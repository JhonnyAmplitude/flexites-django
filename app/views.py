from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema

from .models import CustomUser, Organization
from .serializers import (
    CustomUserGetSerializer,
    LoginSerializer,
    RegistrationSerializer,
    CustomUserPatchSerializer,
    OrganizationSerializer,
    CustomUserSerializer,
    CustomUserPostOrganizationsSerializer,
    OrganizationWithUsersSerializer,
)
from .services import (
    create_organization,
    register_custom_user,
    authenticate_user,
    add_organizations_to_user,
    update_user_profile,
    get_user_by_id,
)

@extend_schema(request=RegistrationSerializer)
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

    @extend_schema(request=CustomUserPatchSerializer)
    def patch(self, request):
        updated_custom_user = update_user_profile(request.user, request.data)
        return Response(updated_custom_user, status=status.HTTP_200_OK)


class CustomUserByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _, user_id):
        user = get_user_by_id(user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    @extend_schema(request=CustomUserPostOrganizationsSerializer)
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

    @extend_schema(request=OrganizationSerializer)
    def post(self, request):
        organization = create_organization(request.data)
        return Response(organization, status=status.HTTP_201_CREATED)