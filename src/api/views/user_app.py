from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from api.serializer.user_app import RegisterSerializer, LoginSerializer, ProfileUpdateSerializer, \
    ChangePhotoProfileSerializer, ProfileSerializer, LogoutSerializer

class RegisterUserApiView(APIView):
    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        if ser.is_valid():
            user = ser.save()
            return Response({
                "user": ser.data,
                "token": user.token()
            }, status=status.HTTP_201_CREATED)
        
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                return Response({
                    "message":"tizimga muvaffaqiyatli kirdingiz!",
                    "username": user.username,
                    "tokens": user.token() 
                }, status=status.HTTP_200_OK)
            
            return Response(
                {"error": "Username yoki parol xato!"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileUpdateApiView(UpdateAPIView):
    http_method_names = ['put', 'patch']
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super(ProfileUpdateApiView,self).update(request, *args, **kwargs)
    
        data = {
            "succes":True,
            "message":"malumotlar yangilandi"

            }
        return Response(data,status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        super(ProfileApiView,self).partial_update(request, *args, **kwargs)
        data = {
            "succes":True,
            "message":"malumotlar yangilandi",
            
            }
        return Response(data,status.HTTP_200_OK)



class ChangePhotoProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self,request,*args,**kwargs):
        ser = ChangePhotoProfileSerializer(data=request.data)
        if ser.is_valid():
            user = request.user
            ser.update(user,ser.validated_data)

            data = {
                "success":True,
                "messge":"progile rasmi muvaffaqiyatli yuklandi"
            }

            return Response(data,status.HTTP_200_OK)
        
        return Response(
            ser.errors,
            status.HTTP_400_BAD_REQUEST
        )



class ProfileApiView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user
    



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get("refresh")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "success": True,
                "message": "Siz logoutni muvaffaqiyatli amalga oshirdingiz!"
            }, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({
                "success": False,
                "message": "Token noto‘g‘ri yoki eskirgan"
            }, status=status.HTTP_400_BAD_REQUEST)