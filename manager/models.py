from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="workers")


class TaskType(models.Model):
    name = models.CharField(max_length=255)


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "URGENT", "Urgent!!!"
        HIGH = "HIGH", "High!"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=9,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")
