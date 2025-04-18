from django import forms
from django.forms.widgets import DateInput

from manager.models import Worker, Task, Position, TaskType
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = '__all__'


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['first_name', 'last_name', 'email', 'position']  # додано тільки необхідні поля

    def clean_position(self):
        position = self.cleaned_data.get('position')
        if not position:
            raise forms.ValidationError('Position must be selected if it is required.')
        return position


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'priority', 'deadline', 'assignees', 'task_type']
        widgets = {
            'deadline': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_assignees(self):
        assignees = self.cleaned_data.get('assignees')
        if not assignees:
            raise forms.ValidationError('At least one assignee must be selected.')
        return assignees
