from apps.task.models import Task, TaskHistory
from api.serializer.task_serializer import TaskSerializer, TaskHistorySerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.utils.paginator import CustomPagination


class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
        task = serializer.save(user=self.request.user)
        # Yaratilgani haqida tarixga yozish
        TaskHistory.objects.create(
            user=self.request.user,
            task=task,
            change_details="Vazifa yaratildi"
        )

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def get_object(self):
        return self.request.user
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskRetrivelUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id' 

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    

class TaskHistoryListView(generics.ListAPIView):
    serializer_class = TaskHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


    def get_queryset(self):
        return TaskHistory.objects.filter(user=self.request.user).order_by('-changed_at')
