from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from manager.forms import TaskTypeForm, WorkerForm, TaskForm
from manager.models import Worker, Task, Position, TaskType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_tasks = user.tasks.select_related("task_type").all()

        upcoming_user_tasks = user_tasks.filter(
            deadline__gte=now(),
            is_completed=False
        ).order_by("deadline")[:3]

        task_priority_count = {
            "Urgent": user_tasks.filter(priority="URGENT").count(),
            "High": user_tasks.filter(priority="HIGH").count(),
            "Medium": user_tasks.filter(priority="MEDIUM").count(),
            "Low": user_tasks.filter(priority="LOW").count(),
        }

        context.update({
            "total_tasks": user_tasks.count(),
            "completed_tasks": user_tasks.filter(is_completed=True).count(),
            "upcoming_tasks": upcoming_user_tasks,
            "priority_stats": task_priority_count,
            "oldest_task": user_tasks.filter(is_completed=False).order_by("deadline").first(),
            "current_user": user,
        })
        return context


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = "manager/position_list.html"
    context_object_name = "position_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for position in context["position_list"]:
            workers = position.workers.all()
            position.task_count = sum(
                worker.tasks.filter(is_completed=True).count()
                for worker in workers
            )
        return context


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "manager/type_of_task_list.html"
    paginate_by = 5

    TASK_TYPE_DESCRIPTIONS = {
        "Bug": "Fixing an error or unexpected behavior in the system.",
        "Code Review": "Reviewing code written by "
                       "others to ensure quality and consistency.",
        "Deployment": "Releasing code or features to production or "
                      "staging environments.",
        "Feature": "Developing a new functionality "
                   "or capability in the product.",
        "Figma Collaboration": "Working together on UI/UX "
                               "designs using Figma.",
        "Hiring / Interview": "Participating in recruitment — interviews, "
                              "reviewing CVs or test tasks.",
        "Improvement": "Enhancing existing functionality "
                       "or internal processes.",
        "Meeting": "Team discussions, planning, syncs, or status updates.",
        "Mentorship": "Guiding or helping a colleague grow or solve problems.",
        "Optimization": "Improving performance, "
                        "efficiency, or system architecture.",
        "Planning": "Organizing sprints, "
                    "releases, or long-term product strategy.",
        "Security": "Tasks focused on securing the system, "
                    "such as audits or risk analysis.",
        "Security Patch": "Fixing security vulnerabilities in the codebase.",
        "Testing": "Writing or executing tests to validate software behavior.",
        "UI Design": "Designing user interface elements such as "
                     "buttons, layouts, and visuals.",
        "UX Research": "Analyzing user behavior to improve "
                       "product experience.",
        "VPN Configuration": "Setting up or troubleshooting "
                             "VPN access for secure connectivity.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_type_list"] = TaskType.objects.all()
        context["task_type_description"] = self.TASK_TYPE_DESCRIPTIONS
        return context


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "manager/worker_list.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker_list"] = Worker.objects.exclude(is_superuser=True)
        return context


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    queryset = Worker.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        context["tasks"] = worker.tasks.all()
        return context


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("manager:worker-list")
    template_name = "manager/worker_form.html"


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("manager:worker-list")
    template_name = "manager/worker_form.html"


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")
    template_name = "manager/worker_confirm_delete.html"


class TaskListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Task
    queryset = Task.objects.select_related()

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_list"] = self.get_queryset()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'manager/task_detail.html'
    context_object_name = 'task'

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()
        return redirect('manager:task-detail', pk=task.pk)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_form.html"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_form.html"


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_confirm_delete.html"
