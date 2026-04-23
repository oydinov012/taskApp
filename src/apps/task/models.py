from django.db import models
from apps.users.models import User

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}  {self.name}"
    


class TaskHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.Case, related_name='history')

    def __str__(self):
        return f"{self.user.username} {self.task}"