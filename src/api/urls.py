from api.views.user_app import RegisterUserApiView, LoginView, ProfileApiView ,ChangePhotoProfileView
from django.urls import path, include

urlpatterns=[
    path('login/',LoginView.as_view()),
    path('register/',RegisterUserApiView.as_view()),
    path('profile/',ProfileApiView.as_view()),
    path('photo/',ChangePhotoProfileView.as_view())
]

