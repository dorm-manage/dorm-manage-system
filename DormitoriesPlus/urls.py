from django.urls import path
from . import views

urlpatterns = [
    # Root URL - add this line to handle the empty path
    path('', views.login_page, name='login_page'),

    # Authentication URLs
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.custom_logout, name='logout'),

    # Existing URLs
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
    path('BM_inventory/', views.BM_inventory, name='BM_inventory'),
    path('BM_loan_requests/', views.BM_loan_requests, name='BM_loan_requests'),
    path('BM_manage_students/', views.BM_manage_students, name='BM_manage_students'),

    # Office Manager URLs
    path('OM_manage_BM/', views.OM_manage_BM, name='OM_manage_BM'),
    path('OM_Homepage/', views.OM_Homepage, name='OM_Homepage'),
    path('OM_inventory/', views.OM_inventory, name='OM_inventory'),
    path('OM_loan_requests/', views.OM_loan_requests, name='OM_loan_requests'),
    path('OM_faults/', views.OM_faults, name='OM_faults'),
    path('OM_manage_students/', views.OM_manage_students, name='OM_manage_students'),
]