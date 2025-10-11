from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class AuthenticationRequestSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'}
    )

    def validate_username(self, value):
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

