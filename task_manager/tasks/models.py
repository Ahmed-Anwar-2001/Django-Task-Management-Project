from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Photo(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Foreign key referencing Task model
    image = models.ImageField(upload_to='task_photos/')

    def __str__(self):
        return f'Photo ID: {self.id} - Task ID: {self.task.id}'
