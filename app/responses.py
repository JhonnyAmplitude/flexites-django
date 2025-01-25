from rest_framework.response import Response
from rest_framework import status


def registration_successful_response(user):
    """Формирует успешный ответ при регистрации пользователя."""
    return Response(
        {
            "message": "Пользователь успешно создан.",
            "user_id": user.id,
        },
        status=status.HTTP_201_CREATED,
    )

def login_successful_response(tokens):
    """
    Формирует успешный ответ для логина.
    Возвращает access и refresh токены.
    """
    return Response(
        {
            "refresh": tokens['refresh'],
            "access": tokens['access'],
        },
        status=status.HTTP_200_OK,
    )

def organization_created_response(organization):
    """Формирует успешный ответ при создании организации."""
    return Response(
        {
            "message": "Организация успешно создана.",
            "organization_id": organization.id,
            "name": organization.name,
        },
        status=status.HTTP_201_CREATED,
    )

def success_response(message):
    """
    Формирует успешный ответ с сообщением.
    """
    return Response({"message": message}, status=status.HTTP_200_OK)

def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Формирует ошибочный ответ с сообщением.
    """
    return Response({"error": message}, status=status_code)


def organizations_list_success_response(data, status_code=status.HTTP_200_OK):
    """
    Формирует успешный ответ с переданными данными.
    """
    return Response(data, status=status_code)


def user_profile_update_success_response(data, status_code=status.HTTP_200_OK):
    """
    Формирует успешный ответ с переданными данными.
    """
    return Response(data, status=status_code)

def user_profile_update_error_response(errors, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Формирует ошибочный ответ с переданными ошибками.
    """
    return Response(errors, status=status_code)