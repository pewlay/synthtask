from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from manager.models import Worker, Task, Position, TaskType


@login_required
def home(request: HttpRequest) -> HttpResponse:
    context = {
        "num_workers": Worker.objects.count(),
        "num_tasks": Task.objects.count(),
    }

    return render(request, 'manager/home.html', context=context)


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = "manager/position_list.html"
    context_object_name = "position_list"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for position in context["position_list"]:
            workers = position.workers.all()
            position.task_count = sum(
                worker.tasks.filter(is_completed=True).count()
                for worker in workers
            )
        return context


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")
    template_name = "manager/position_form.html"


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")
    template_name = "manager/position_form.html"


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy("manager:position-list")
    template_name = "manager/position_confirm_delete.html"


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "manager/type_of_task_list.html"
    paginate_by = 5

    TASK_TYPE_DESCRIPTIONS = {
        "Bug": "Fixing an error or unexpected behavior in the system.",
        "Code Review": "Reviewing code written by others to ensure quality and consistency.",
        "Deployment": "Releasing code or features to production or staging environments.",
        "Feature": "Developing a new functionality or capability in the product.",
        "Figma Collaboration": "Working together on UI/UX designs using Figma.",
        "Hiring / Interview": "Participating in recruitment — interviews, reviewing CVs or test tasks.",
        "Improvement": "Enhancing existing functionality or internal processes.",
        "Meeting": "Team discussions, planning, syncs, or status updates.",
        "Mentorship": "Guiding or helping a colleague grow or solve problems.",
        "Optimization": "Improving performance, efficiency, or system architecture.",
        "Planning": "Organizing sprints, releases, or long-term product strategy.",
        "Security": "Tasks focused on securing the system, such as audits or risk analysis.",
        "Security Patch": "Fixing security vulnerabilities in the codebase.",
        "Testing": "Writing or executing tests to validate software behavior.",
        "UI Design": "Designing user interface elements such as buttons, layouts, and visuals.",
        "UX Research": "Analyzing user behavior to improve product experience.",
        "VPN Configuration": "Setting up or troubleshooting VPN access for secure connectivity.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_type_list"] = TaskType.objects.all()
        context["task_type_description"] = self.TASK_TYPE_DESCRIPTIONS
        return context


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("manager:task_type-list")
    template_name = "manager/tasktype_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("manager:task_type-list")
    template_name = "manager/tasktype_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    success_url = reverse_lazy("manager:task_type-list")
    template_name = "manager/tasktype_confirm_delete.html"


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "manager/worker_list.html"
    paginate_by = 8

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
    fields = "__all__"
    success_url = reverse_lazy("manager:worker-list")
    template_name = "manager/worker_form.html"


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    fields = "__all__"
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_list"] = Task.objects.all()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    queryset = Task.objects.select_related()


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_form.html"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_form.html"


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_confirm_delete.html"
