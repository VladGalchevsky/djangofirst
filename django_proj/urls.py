"""django_proj URL Configuration

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
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from students.views import groups, students, journal


urlpatterns = [
    # Students urls
path('', students.students_list, name='home'),
path('students/add/', students.students_add,
name='students_add'),
path('students/<int:sid>/edit/',
students.students_edit,
name='students_edit'),
path('students/<int:sid>/delete/',
students.students_delete,
name='students_delete'),

    # Groups urls
path('groups/', groups.groups_list, name='groups'),
path('groups/add/', groups.groups_add,
name='groups_add'),
path('groups/<int:gid>/edit/',
groups.groups_edit,
name='groups_edit'),
path('groups/<int:gid>/delete/',
groups.groups_delete,
name='groups_delete'),

# Journal urls
path('journal/', journal.journal_list, name="journal"),
path('journal/<int:jid>/', journal.journal_jid, name="journal_jid"),
path('journal/update', journal.journal_update, name="journal_update"),

path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

