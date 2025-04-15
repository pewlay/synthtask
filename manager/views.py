from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from manager.models import Worker, Task


def home(request: HttpRequest) -> HttpResponse:
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
    }

    return render(request, "manager/home.html", context=context)
