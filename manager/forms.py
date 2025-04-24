from django import forms
from django.forms.widgets import DateTimeInput
from django.utils.timezone import now

from manager.models import Worker, Task, Position, TaskType


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
        fields = [
            'first_name',
            'last_name',
            'email',
            'position'
        ]

    def clean_position(self):
        position = self.cleaned_data.get('position')
        if not position:
            raise forms.ValidationError(
                'Position must be selected if it is required.'
            )
        return position


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'priority',
            'deadline',
            'assignees',
            'task_type'
        ]
        widgets = {
            'deadline': DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('deadline'):
            self.initial['deadline'] = self.initial[
                'deadline'
            ].strftime('%Y-%m-%dT%H:%M')

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < now():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline

    def clean_assignees(self):
        assignees = self.cleaned_data.get('assignees')
        if not assignees:
            raise forms.ValidationError(
                'At least one assignee must be selected.'
            )
        return assignees
