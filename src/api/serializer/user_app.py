from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.contrib.auth import authenticate
from django.core.validators import FileExtensionValidator

from apps.users.models import User
from apps.utils.utility import validate_uz_phone, normalize_uz_phone


# =========================
# USER OUTPUT
# =========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone',
            'photo'
        ]


# =========================
# REGISTER
# =========================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# =========================
# LOGIN (JWT READY)
# =========================
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs.get("username"),
            password=attrs.get("password")
        )

        if not user:
            raise AuthenticationFailed("Username yoki parol noto‘g‘ri")

        attrs["user"] = user
        return attrs


# =========================
# PROFILE UPDATE
# =========================
class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    confirm_password = serializers.CharField(required=False, write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password or confirm_password:
            if not password or not confirm_password:
                raise ValidationError("Ikkala parol ham kiritilishi shart")

            if password != confirm_password:
                raise ValidationError("Parollar mos emas")

        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")

        if first_name and last_name and first_name == last_name:
            raise ValidationError("Ism va familiya bir xil bo‘lmasin")

        return attrs

    def validate_phone(self, value):
        value = normalize_uz_phone(value)
        validate_uz_phone(value)
        return value

    def update(self, instance, validated_data):
        for field in ["first_name", "last_name", "username", "phone"]:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        instance.save()
        return instance


# =========================
# PROFILE GET
# =========================
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'phone',
            'photo'
        ]


# =========================
# PHOTO UPDATE
# =========================
class ChangePhotoProfileSerializer(serializers.Serializer):
    photo = serializers.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "jpg", "heic", "heif", "png"]
            )
        ]
    )

    def update(self, instance, validated_data):
        instance.photo = validated_data.get("photo", instance.photo)
        instance.save()
        return instance


# =========================
# LOGOUT
# =========================
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()