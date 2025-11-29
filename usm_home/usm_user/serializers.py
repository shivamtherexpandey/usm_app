from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from usm_user.models import SubscriptionPlan, Subscription, User


class AuthenticationRequestSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, min_length=8, style={"input_type": "password"}
    )

    def validate_username(self, value):
        return value

    def validate_password(self, value):
        validate_password(value)
        return value


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "is_active"]


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer()

    class Meta:
        model = Subscription
        fields = ["id", "plan", "is_active"]


class UserDetailsSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "subscription",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "subscription",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at",
        ]
