from .serializers import RegistrationSerializer
from rest_framework import serializers

class RegistrationSuccessSerializer(RegistrationSerializer):
    message = serializers.CharField()
    user_id = serializers.IntegerField()