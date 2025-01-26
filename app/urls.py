from django.urls import path
from .views import (
    OrganizationCreateView,
    GetAllOrganizationsWithUsersView,

    register,
    login,
    CustomUserView,
    CustomUserByIdView,
    CustomUsersViewSet,
    OrganizationsViewSet
)


urlpatterns = [
    path('register/', register),
    path('login/', login),

    path('users/me/', CustomUserView.as_view()),
    path('users/<int:user_id>/organizations/', CustomUserByIdView.as_view()),
    path('users/<int:user_id>/organizations/', CustomUserByIdView.as_view()),
    path('users/', CustomUsersViewSet.as_view({'get': 'list'})),

    path('organizations/', OrganizationsViewSet.as_view({'get': 'list'})),
    path('organizations/create/', OrganizationCreateView.as_view()),
    path('organizations/with_users/', GetAllOrganizationsWithUsersView.as_view()),
]
