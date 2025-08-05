from django.urls import path
from . import views
from .api_views import OMSummaryAPIView, OMAISummaryAPIView, GeminiModelsAPIView

urlpatterns = [
    # Root URL - add this line to handle the empty path
    path('', views.login_page, name='login_page'),

    # Authentication URLs
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.custom_logout, name='logout'),

    # Student URLs
    path('student/homepage/', views.Students_homepage, name='Students_homepage'),
    path('student/application/', views.application, name='application'),
    path('student/faults/', views.faults, name='faults'),
    path('student/connect-us/', views.connect_us, name='connect_us'),

    # Building Manager URLs
    path('bm/homepage/', views.BM_Homepage, name='BM_Homepage'),
    path('bm/faults/', views.BM_faults, name='BM_faults'),
    path('bm/send-message/', views.BM_sendMassage, name='BM_sendMassage'),
    path('bm/inventory/', views.BM_inventory, name='BM_inventory'),
    path('bm/loan-requests/', views.BM_loan_requests, name='BM_loan_requests'),
    path('bm/manage-students/', views.BM_manage_students, name='BM_manage_students'),

    # Office Manager URLs
    path('om/homepage/', views.OM_Homepage, name='OM_Homepage'),
    path('om/inventory/', views.OM_inventory, name='OM_inventory'),
    path('om/loan-requests/', views.OM_loan_requests, name='OM_loan_requests'),
    path('om/faults/', views.OM_faults, name='OM_faults'),
    path('om/manage-students/', views.OM_manage_students, name='OM_manage_students'),
    path('om/manage-bm/', views.OM_manage_BM, name='OM_manage_BM'),

    # Legacy URLs (for backward compatibility)
    path('Homepage/', views.Homepage, name='Homepage'),
    path('manager_Homepage/', views.manager_Homepage, name='manager_Homepage'),

    # New URL for OM summary API
    path('api/om-summary/', OMSummaryAPIView.as_view(), name='om_summary_api'),
    path('api/om-ai-summary/', OMAISummaryAPIView.as_view(), name='om_ai_summary_api'),
    path('api/gemini-models/', GeminiModelsAPIView.as_view(), name='gemini_models_api'),

    # Language switcher
    path('set-language/', views.set_language, name='set_language'),
]