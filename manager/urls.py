from django.urls import path
from manager.views import (
    home,
    PositionListView,
    TaskTypeListView,
    WorkerListView,
    WorkerDetailView,
    TaskListView,
    TaskDetailView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)


app_name = 'manager'

urlpatterns = [
    path('', home, name='home'),
    path('positions/', PositionListView.as_view(), name='position-list'),
    path('positions/create/', PositionCreateView.as_view(), name='position-create'),
    path('positions/<int:pk>/update/', PositionUpdateView.as_view(), name='position-update'),
    path('positions/<int:pk>/delete/', PositionDeleteView.as_view(), name='position-delete'),
    path('types/', TaskTypeListView.as_view(), name='task_type-list'),
    path('types/create/', TaskTypeCreateView.as_view(), name='task_type-create'),
    path('types/<int:pk>/update/', TaskTypeUpdateView.as_view(), name='task_type-update'),
    path('types/<int:pk>/delete/', TaskTypeDeleteView.as_view(), name='task_type-delete'),
    path('workers/', WorkerListView.as_view(), name='worker-list'),
    path('workers/<int:pk>/', WorkerDetailView.as_view(), name='worker-detail'),
    path('workers/create/', WorkerCreateView.as_view(), name='worker-create'),
    path('workers/<int:pk>/update/', WorkerUpdateView.as_view(), name='worker-update'),
    path('workers/<int:pk>/delete/', WorkerDeleteView.as_view(), name='worker-delete'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/<int:pk>/toggle-status/', TaskDetailView.as_view(), name='toggle-task-status'),
]

