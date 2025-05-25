"""
URL configuration for DormitoriesPlus_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from DormitoriesPlus import views

# Language switching URL pattern
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# URL patterns with language prefix
urlpatterns += i18n_patterns(
    path('', views.login_page, name='login_page'),
    path('admin/', admin.site.urls),
    path('Homepage/', views.Homepage, name='Homepage'),
    path('Students_homepage/', views.Students_homepage, name='Students_homepage'),
    path('application/', views.application, name='application'),
    path('faults/', views.faults, name='faults'),
    path('legal_assistance/', views.legal_assistance, name='legal_assistance'),
    path('connect_us/', views.connect_us, name='connect_us'),
    path('accessibility/', views.accessibility, name='accessibility'),
    path('accessibility/contact/', views.accessibility_contact, name='accessibility_contact'),
    path('logout/', views.custom_logout, name='logout'),
    path('OM_Homepage/', views.OM_Homepage, name='OM_Homepage'),
    path('Student_Profile/', views.Student_Profile, name='Student_Profile'),
    path('OM_Profile/', views.OM_Profile, name='OM_Profile'),
    path('Student_Profile/Edit_Profile/', views.Edit_Profile, name='Edit_Profile'),
    path('OM_Profile/Edit_Profile/', views.Edit_Profile, name='Edit_Profile'),
    path('Student_Profile/Edit_Profile/Change_Password/', views.Change_Password, name='Change_Password'),
    path('OM_Profile/Edit_Profile/Change_Password/', views.Change_Password, name='Change_Password'),
    path('Student_Profile/Edit_Profile/Change_Password/Password_Changed/', views.Password_Changed, name='Password_Changed'),
    path('OM_Profile/Edit_Profile/Change_Password/Password_Changed/', views.Password_Changed, name='Password_Changed'),
    path('Student_Profile/Edit_Profile/Profile_Updated/', views.Profile_Updated, name='Profile_Updated'),
    path('OM_Profile/Edit_Profile/Profile_Updated/', views.Profile_Updated, name='Profile_Updated'),
    path('Student_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/', views.Back_to_Profile, name='Back_to_Profile'),
    path('OM_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/', views.Back_to_Profile, name='Back_to_Profile'),
    path('Student_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/Edit_Profile/', views.Edit_Profile, name='Edit_Profile'),
    path('OM_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/Edit_Profile/', views.Edit_Profile, name='Edit_Profile'),
    path('Student_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/Change_Password/', views.Change_Password, name='Change_Password'),
    path('OM_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/Change_Password/', views.Change_Password, name='Change_Password'),
    path('Student_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/Logout/', views.custom_logout, name='logout'),
    path('OM_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/Logout/', views.custom_logout, name='logout'),
    path('Student_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/Back_to_Homepage/', views.Back_to_Homepage, name='Back_to_Homepage'),
    path('OM_Profile/Edit_Profile/Profile_Updated/Back_to_Profile/Back_to_Homepage/', views.Back_to_Homepage, name='Back_to_Homepage'),
    prefix_default_language=False
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)