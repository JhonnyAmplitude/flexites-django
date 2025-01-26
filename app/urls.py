from django.urls import path
from .views import (
    CustomUserView,
    OrganizationCreateView,
    OrganizationListView,
    AddOrganizationsToUserView,
    UserOrganizationsView,
    GetAllOrganizationsWithUsersView,
    GetUsersAndTheirOrganizationsViewSet,
    register,
    login
)


urlpatterns = [
    path('register/', register, name='user-register'),
    path('login/', login, name='user-login'),

    path('users/me/', CustomUserView.as_view(), name='profile-update'),
    path('users/', GetUsersAndTheirOrganizationsViewSet.as_view({'get': 'list'}), name='users-list'),
    path('users/<int:user_id>/add_organizations/', AddOrganizationsToUserView.as_view()),
    path('users/<int:user_id>/organizations/', UserOrganizationsView.as_view()),

    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('organizations/create/', OrganizationCreateView.as_view(), name='organization-create'),
    path('organizations/with_users/', GetAllOrganizationsWithUsersView.as_view()),
]
