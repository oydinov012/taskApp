from rest_framework import serializers
from apps.task.models import Task, TaskHistory
from api.serializer.user_app import UserSeralizer


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    # user = UserSeralizer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            # "user",
            "name",
            "description",
            "deadline",
            "is_completed"
        ]


class TaskHistorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSeralizer(read_only=True)

    class Meta:
        model = TaskHistory
        fields = "__all__"


