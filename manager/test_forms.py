from django.test import TestCase
from manager.forms import PositionForm, TaskTypeForm, WorkerForm, TaskForm
from manager.models import Worker, Position, TaskType


class PositionFormTest(TestCase):
    def test_position_form_valid(self):
        position_data = {'name': 'Developer'}
        form = PositionForm(data=position_data)
        self.assertTrue(form.is_valid())

    def test_position_form_invalid(self):
        form = PositionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class TaskTypeFormTest(TestCase):
    def test_task_type_form_valid(self):
        task_type_data = {'name': 'Bug Fix'}
        form = TaskTypeForm(data=task_type_data)
        self.assertTrue(form.is_valid())

    def test_task_type_form_invalid(self):
        form = TaskTypeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class WorkerFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_worker_form_valid(self):
        worker_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'position': self.position.id
        }
        form = WorkerForm(data=worker_data)
        self.assertTrue(form.is_valid())



class TaskFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bug Fix")


    def test_task_form_invalid(self):
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('assignees', form.errors)
