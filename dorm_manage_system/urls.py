from django.urls import path
from . import views

urlpatterns = [
    path('legal_assistance/', views.legal_assistance, name='legal_assistance'),
    path('connect_us/', views.connect_us, name='connect_us'),
    path('accessibility/', views.accessibility, name='accessibility'),
    path('accessibility/contact/', views.accessibility_contact, name='accessibility_contact'),
] 