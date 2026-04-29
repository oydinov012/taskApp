from api.views.user_app import RegisterUserApiView, LoginView, ProfileUpdateApiView ,\
    ChangePhotoProfileView, ProfileApiView, LogoutView
from api.views.task_view import TaskDetailView, TaskHistoryListView, TaskListCreateView
from django.urls import path, include

urlpatterns=[
    path('login/',LoginView.as_view()),
    path('register/',RegisterUserApiView.as_view()),
    path('profile/',ProfileApiView.as_view()) ,
    path('profile-edit/',ProfileUpdateApiView.as_view()),
    path('photo/',ChangePhotoProfileView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('history/',TaskHistoryListView.as_view()),
    path('tasks/',TaskListCreateView.as_view()),
    path('tasks/<uuid:id>/', TaskDetailView.as_view()),
]

