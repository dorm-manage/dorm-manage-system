from django.urls import path
from . import views

urlpatterns = [
    # Root URL - add this line to handle the empty path
    path('', views.login_page, name='login_page'),

    # Authentication URLs
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.custom_logout, name='logout'),

    # Legal Assistance URL
    path('legal-assistance/', views.legal_assistance, name='legal_assistance'),

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
    path('bm/loan-requests/', views.BM_loan_requests, name='BM_loan_requests'),
    path('bm/manage-students/', views.BM_manage_students, name='BM_manage_students'),

    # Office Manager URLs
    path('manager/bm/', views.OM_manage_BM, name='OM_manage_BM'),
    path('om/homepage/', views.OM_Homepage, name='OM_Homepage'),
    path('om/inventory/', views.OM_inventory, name='OM_inventory'),
    path('om/loan_requests/', views.OM_loan_requests, name='OM_loan_requests'),
    path('om/faults/', views.OM_faults, name='OM_faults'),
    path('om/manage_students/', views.OM_manage_students, name='OM_manage_students'),
]