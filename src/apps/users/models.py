from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractUser):
    phone=models.CharField(max_length=30,blank=True,null=True)
    photo = models.ImageField(upload_to="static/user_photos/",null=True,blank=True,  validators=[FileExtensionValidator(allowed_extensions=["jpeg","jpg","heic","heif","png"])])


    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access":str(refresh.access_token),
            "refresh_token":str(refresh)
        }


    def __str__(self):
        return self.username