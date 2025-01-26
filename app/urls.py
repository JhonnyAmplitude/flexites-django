from django.urls import path
from .views import (
    LoginView,
    ProfileUpdateView,
    OrganizationCreateView,
    OrganizationListView,
    AddOrganizationsToUserView,
    UserOrganizationsView,
    GetAllOrganizationsWithUsersView,
    GetUsersAndTheirOrganizationsViewSet,
    register
)


urlpatterns = [
    path('register/', register, name='user-register'),
    path('login/', LoginView.as_view(), name='login'),

    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('organizations/create/', OrganizationCreateView.as_view(), name='organization-create'),
    path('organizations/with_users/', GetAllOrganizationsWithUsersView.as_view()),

    path('users/me/', ProfileUpdateView.as_view(), name='profile-update'),
    path('users/', GetUsersAndTheirOrganizationsViewSet.as_view({'get': 'list'}), name='users-list'),
    path('users/<int:user_id>/add_organizations/', AddOrganizationsToUserView.as_view()),
    path('users/<int:user_id>/organizations/', UserOrganizationsView.as_view()),
]
