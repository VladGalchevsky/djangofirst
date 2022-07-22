"""students_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from students.views import groups, students, journal, contact_admin

urlpatterns = [
    # Students urls
    path('', students.students_list, name='home'),
    path('students/add/', students.students_add,
         name='students_add'),
    path('students/<int:pk>/edit/',
         students.StudentUpdateView.as_view(),
         name='students_edit'),
    path('students/<int:pk>/delete/',
         students.StudentDeleteView.as_view(),
         name='students_delete'),

    # Groups urls
    path('groups/', groups.groups_list, name='groups'),
    path('groups/add/', groups.GroupAddView.as_view(),
         name='groups_add'),
    path('groups/<int:pk>/edit/',
         groups.GroupUpdateView.as_view(),
         name='groups_edit'),
    path('groups/<int:pk>/delete/',
         groups.GroupDeleteView.as_view(),
         name='groups_delete'),

    # Journal urls
    re_path(r'journal/(?:(?P<pk>\d+)/)?$', journal.JournalView.as_view(),
            name='journal'),

    # Contact Admin Form
    path('contact-admin/', contact_admin.contact_admin,
         name='contact_admin'),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
