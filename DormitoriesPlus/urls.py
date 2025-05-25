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
    path('OM_Homepage/', views.OM_Homepage, name='OM_Homepage'),
    path('OM_inventory/', views.OM_inventory, name='OM_inventory'),
    path('OM_loan_requests/', views.OM_loan_requests, name='OM_loan_requests'),
    path('OM_faults/', views.OM_faults, name='OM_faults'),
    path('OM_manage_students/', views.OM_manage_students, name='OM_manage_students'),
    path('OM_manage_BM/', views.OM_manage_BM, name='OM_manage_BM'),
    path('OM_add_building/', views.OM_add_building, name='OM_add_building'),
    
    # Student Management URLs
    path('om/add_student/', views.add_student, name='add_student'),
    path('om/edit_student/', views.edit_student, name='edit_student'),
    path('om/delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('get_rooms/<int:building_id>/', views.get_rooms, name='get_rooms'),
    
    # Building Manager Management URLs
    path('om/add_building_manager/', views.add_building_manager, name='add_building_manager'),
    path('om/edit_building_manager/', views.edit_building_manager, name='edit_building_manager'),
    path('om/delete_building_manager/<int:manager_id>/', views.delete_building_manager, name='delete_building_manager'),
    
    # Room Management URLs
    path('manage_rooms/<int:building_id>/', views.manage_rooms, name='manage_rooms'),
    path('add_room/<int:building_id>/', views.add_room, name='add_room'),
    path('edit_room/<int:building_id>/', views.edit_room, name='edit_room'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('assign_student/', views.assign_student, name='assign_student'),
    path('remove_student/<int:assignment_id>/', views.remove_student, name='remove_student'),
]