from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('autocomplete/', views.city_autocomplete, name='city-autocomplete'),
]