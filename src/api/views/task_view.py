from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.task.models import Task, TaskHistory
from api.serializer.task_serializer import TaskHistorySerializer, TaskSerializer
from apps.utils.paginator import CustomPagination


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)

        TaskHistory.objects.create(
            user=self.request.user,
            task=task,
            change_details="Vazifa yaratildi"
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        task = serializer.save()

        TaskHistory.objects.create(
            user=self.request.user,
            task=task,
            change_details="Vazifa yangilandi"
        )

    def perform_destroy(self, instance):
        TaskHistory.objects.create(
            user=self.request.user,
            task=instance,
            change_details="Vazifa o'chirildi"
        )
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response({
            "success": True,
            "message": "task o'chirildi!!"
        })
    


class TaskHistoryListView(generics.ListAPIView):
    serializer_class = TaskHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return TaskHistory.objects.filter(
            user=self.request.user
        ).order_by('-changed_at')