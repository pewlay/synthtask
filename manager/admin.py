from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from manager.models import Position, Worker, Task, TaskType


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("first_name", "last_name", "position", )
    fieldsets = UserAdmin.fieldsets + ((
        "Additional info", {"fields": ("position",)}
    ),)
    add_fieldsets = UserAdmin.add_fieldsets + ((
        "Additional info", {"fields": ("first_name", "last_name", "position",)}
    ),)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ["name", "priority", ]
    search_fields = ["name", ]


admin.site.register(Position)


admin.site.register(TaskType)
