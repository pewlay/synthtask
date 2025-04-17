from django.urls import path
from manager.views import (
    home,
    PositionListView,
    TaskTypeListView,
    WorkerListView,
    WorkerDetailView,
    TaskListView,
    TaskDetailView,
)


app_name = 'manager'

urlpatterns = [
    path('', home, name='home'),
    path('positions/', PositionListView.as_view(), name='position-list'),
    path('types/', TaskTypeListView.as_view(), name='task_type-list'),
    path('workers/', WorkerListView.as_view(), name='worker-list'),
    path('workers/<int:pk>/', WorkerDetailView.as_view(), name='worker-detail'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]

