from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from manager.models import Position, TaskType, Task


class ModelTests(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Fix login bug",
            description="Fix the login form validation",
            deadline=timezone.now() + timezone.timedelta(days=2),
            priority=Task.Priority.HIGH,
            task_type=self.task_type
        )
        self.task.assignees.add(self.worker)

    def test_task_assignees(self):
        self.assertIn(self.worker, self.task.assignees.all())
