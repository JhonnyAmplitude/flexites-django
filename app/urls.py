from .views import (LoginView, ProfileUpdateView, OrganizationCreateView, OrganizationListView
, AddOrganizationsToUserView, UserOrganizationsView,
                    GetAllOrganizationsWithUsersView,
                    RegistrationView, GetUsersAndTheirOrganizationsViewSet)
from django.urls import path


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='user-register'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('login/', LoginView.as_view(), name='login'),
    path('organizations/create/', OrganizationCreateView.as_view(), name='organization-create'),
    path('users/<int:user_id>/add_organizations/', AddOrganizationsToUserView.as_view()),
    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('users/', GetUsersAndTheirOrganizationsViewSet.as_view({'get': 'list'}), name='users-list'),
    path('users/<int:user_id>/organizations/', UserOrganizationsView.as_view()),
    path('organizations/with_users/', GetAllOrganizationsWithUsersView.as_view()),
]
