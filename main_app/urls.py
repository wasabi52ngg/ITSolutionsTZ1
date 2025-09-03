from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('deals/', views.deals_list, name='deals_list'),
    path('deals/create/', views.DealCreateView.as_view(), name='deal_create'),
]
