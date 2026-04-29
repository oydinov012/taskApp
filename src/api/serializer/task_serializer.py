from rest_framework import serializers
from apps.task.models import Task, TaskHistory

class TaskHistorySerializer(serializers.ModelSerializer):
    # Task nomini ko'rsatish tarixni o'qishda qulay
    task_name = serializers.ReadOnlyField(source='task.name')

    class Meta:
        model = TaskHistory
        fields = [
            "id",
            "task_name",
            "change_details",
            "changed_at"
        ]

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            # "deadline",
            "is_completed"
        ]

    def update(self, instance, validated_data):
        # O'zgarishlarni aniqlash
        old_status = "Bajarilgan" if instance.is_completed else "Bajarilmagan"
        instance = super().update(instance, validated_data)
        new_status = "Bajarilgan" if instance.is_completed else "Bajarilmagan"

        # Agar status o'zgargan bo'lsa, tarixga yozamiz
        if old_status != new_status:
            TaskHistory.objects.create(
                user=instance.user,
                task=instance,
                change_details=f"Holat o'zgardi: {old_status} -> {new_status}"
            )
        return instance 




