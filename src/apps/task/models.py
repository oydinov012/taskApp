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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, related_name='history')
    change_details = models.TextField(blank=True, null=True) 
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.task.name} "