from django.urls import path
from .views import (
    OrganizationCreateView,
    OrganizationListView,
    GetAllOrganizationsWithUsersView,

    register,
    login,
    CustomUserView,
    CustomUserByIdView,
    CustomUsersViewSet,
)


urlpatterns = [
    path('register/', register),
    path('login/', login),

    path('users/me/', CustomUserView.as_view()),
    path('users/<int:user_id>/organizations/', CustomUserByIdView.as_view()),
    path('users/<int:user_id>/organizations/', CustomUserByIdView.as_view()),
    path('users/', CustomUsersViewSet.as_view({'get': 'list'})),

    path('organizations/', OrganizationListView.as_view()),
    path('organizations/create/', OrganizationCreateView.as_view()),
    path('organizations/with_users/', GetAllOrganizationsWithUsersView.as_view()),
]
