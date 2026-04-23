
from rest_framework import serializers
from apps.users.models import User
from rest_framework.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from apps.utils.utility import validate_uz_phone, normalize_uz_phone


class UserSeralizer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 
            # 'email', 
            # 'phone_number',
            'password'
            ]


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class ProfileUpdateSerializer(serializers.Serializer):

    first_name = serializers.CharField(write_only=True,required=True)
    last_name = serializers.CharField(write_only=True,required=True)
    username = serializers.CharField(write_only=True,required=True)
    phone = serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)
    confirm_password = serializers.CharField(write_only=True,required=True)


    def validate(self,attr):
        username = attr.get('username',None)
        password = attr.get('password',None)
        confirm_password = attr.get('confirm_password', None)
        first_name = attr.get('first_name', None)
        last_name = attr.get('last_name', None)

        if not username:
            raise ValidationError(
                "usename mavjud emas"
            )
        
        
        if not password:
            raise ValidationError(
                {
                    "message":"parol kiritilishi majburiy"
                }
            )
        if not confirm_password:
            raise ValidationError(
                {
                    "message":" tasdiqlash parolini ham kiriting !! "
                }
            )
            

        if password != confirm_password:
            raise ValidationError(
                {
                                    "message":"dastlabki va tasdiqlash kodlari bir xil bo'lishi mumkin emas"

                }
            )
        
        if first_name == last_name:
            raise ValidationError(
                {
                    "message":"ism va familiya bir xil!!"
                }
            )
        
        return attr
    def validate_phone(self, value):
        value = normalize_uz_phone(value)
        validate_uz_phone(value)
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name) 
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.password = validated_data.get('password',instance.password)
        instance.username = validated_data.get('username',instance.username) 
        instance.photo = validated_data.get('photo',instance.photo)
        instance.phone = validated_data.get('phone',instance.phone)

        instance.save()
        return instance


        
class ChangePhotoProfileSerializer(serializers.Serializer):
    photo = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=["jpeg","jpg","heic","heif","png"])])

    def update(self, instance, validated_data):
        instance.photo = validated_data.get('photo',instance.photo)
        instance.save()
        return instance



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'phone',
            "password",
            'photo'
        ]


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
