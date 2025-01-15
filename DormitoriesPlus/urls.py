from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('application/', views.application, name='application'),
    path('faults/', views.faults, name='faults'),
    path('connect_us/', views.connect_us, name='connect_us'),
]
