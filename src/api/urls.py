from api.views.user_app import RegisterUserApiView, LoginView, ProfileUpdateApiView ,\
    ChangePhotoProfileView, ProfileApiView, LogoutView
from api.views.task_view import TaskCreateView, TaskListView, TaskRetrivelUpdateDeleteView
from django.urls import path, include

urlpatterns=[
    path('login/',LoginView.as_view()),
    path('register/',RegisterUserApiView.as_view()),
    path('profile/',ProfileApiView.as_view()) ,
    path('profile-edit/',ProfileUpdateApiView.as_view()),
    path('photo/',ChangePhotoProfileView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('task-create/',TaskCreateView.as_view()),
    path('',TaskListView.as_view()),
    path('tasks/<int:id>/', TaskRetrivelUpdateDeleteView.as_view(), name='task-detail'),

]

