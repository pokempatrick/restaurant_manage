from rest_framework import serializers
from authentification.models import User


class RegisterSerilizer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerilizer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "token", "username")

        read_only_fields = ["token"]


class UserSerialiser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "username", "last_name", "first_name",
                  "created_at", "updated_at", "role_name", "added_by", "updated_by")
        read_only_fields = ['created_at',
                            'updated_at', "added_by", "updated_by"]

    def validate_role_name(self, value):
        if value in ['ROLE_ADMIN', 'ROLE_SUPER_ADMIN', 'ROLE_MANAGER']:
            user = self.context["request"].user
            if not user.role_name in ['ROLE_ADMIN', 'ROLE_SUPER_ADMIN']:
                raise serializers.ValidationError(
                    "Only Admin can perform this action.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
