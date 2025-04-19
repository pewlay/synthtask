from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ("-position", "first_name", "last_name", )

    def __str__(self):
        return (f"{self.first_name} {self.last_name} "
                f"(Position: {self.position})")


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


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
        max_length=10,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks"
    )

    class Meta:
        ordering = ("priority", "-deadline", "name")

    def __str__(self):
        return (f"{self.name} Priority: {self.priority} \n"
                f"Deadline: {self.deadline.strftime('%Y-%m-%d %H:%M')} \n"
                f"{'Done' if self.is_completed else 'Not finished'}")
