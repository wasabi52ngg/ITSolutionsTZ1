from django.urls import path
from . import views

app_name = 'start'

urlpatterns = [
    path('', views.start, name='start'),
    path('home/', views.home, name='home'),
    path('recreate-priority-field/', views.recreate_priority_field, name='recreate_priority_field'),
]
