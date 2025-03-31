from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_page, name='login_page'),
    path('logout/', views.custom_logout, name='logout'),
    path('Homepage/', views.Homepage, name='Homepage'),
    path('application/', views.application, name='application'),
    path('faults/', views.faults, name='faults'),
    path('connect_us/', views.connect_us, name='connect_us'),
    path('Personal_erea/', views.Personal_erea, name='personal_erea'),
    path('manager_Homepage/', views.manager_Homepage, name='manager_Homepage'),
    path('BM_Homepage/', views.BM_Homepage, name='BM_Homepage'),
    path('Students_homepage/', views.Students_homepage, name='Students_homepage'),
    path('BM_faults/', views.BM_faults, name='BM_faults'),
    path('BM_sendMassage/', views.BM_sendMassage, name='BM_sendMassage'),
    path('manage_room/', views.manage_room, name='manage_room'),
    path('manager_inventory/', views.manager_inventory, name='manager_inventory'),
    path('manager_BM/', views.manager_BM, name='manager_BM'),
    path('Manager_request/', views.Manager_request, name='Manager_request'),
    path('manager_faults/', views.manager_faults, name='manager_faults'),








]
