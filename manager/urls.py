from django.urls import path
from manager.views import home


app_name = 'manager'

urlpatterns = [
    path('', home, name='home')
]

