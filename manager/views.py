from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from manager.models import Worker, Task, Position, TaskType


def home(request: HttpRequest) -> HttpResponse:
    context = {
        "num_workers": Worker.objects.count(),
        "num_tasks": Task.objects.count(),
    }

    return render(request, 'manager/home.html', context=context)


class PositionListView(ListView):
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


class TaskTypeListView(ListView):
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


class WorkerListView(ListView):
    model = Worker
    template_name = "manager/worker_list.html"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker_list"] = Worker.objects.exclude(is_superuser=True)
        return context


class WorkerDetailView(DetailView):
    model = Worker
    queryset = Worker.objects.select_related()


class TaskListView(ListView):
    paginate_by = 5
    model = Task
    queryset = Task.objects.select_related()


class TaskDetailView(DetailView):
    model = Task
    queryset = Task.objects.select_related()
