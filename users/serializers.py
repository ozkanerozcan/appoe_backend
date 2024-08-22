from django.contrib.auth import authenticate
from rest_framework import serializers
from django.conf import settings
from django.core.validators import RegexValidator

from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """
    avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "avatar", "bio", "is_active", "first_name", "last_name")


    def get_avatar(self, obj):
        if obj.avatar:
            return settings.WEBSITE_URL + obj.avatar.url
        else:
            return 'https://picsum.photos/200/200'



class UserRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,}$',
                message="At least 8 characters long, Contains at least one uppercase letter, lowercase letter, one digit, one special character (e.g., @, #, $, etc.)",
                code="invalid_registration",
            ),
        ],
    )

    avatar = serializers.SerializerMethodField('get_avatar')

    def get_avatar(self, obj):
        if obj.avatar:
            return settings.WEBSITE_URL + obj.avatar.url
        else:
            return 'https://picsum.photos/200/200'

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user

        if user and not user.is_active:
            raise serializers.ValidationError("User is not active")

        raise serializers.ValidationError("Credentials are incorrect ")


class UserEditSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the details
    """

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "bio")

class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the avatar
    """

    class Meta:
        model = CustomUser
        fields = ("avatar", )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(["New passwords don't match."])
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(["Old password is not correct."])
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
