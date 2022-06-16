from django.shortcuts import render
from django.http import HttpResponse


# Views for Groups
def groups_list(request):
    groups = (
        {'id': 1,
         'name': 'Мтм-21',
         'leader': {'id': 1, 'name': 'Літвінов Дмитро'}},
        {'id': 2,
         'name': 'Мтм-22',
         'leader': {'id': 2, 'name': 'Віталій Подоба'}},
        {'id': 3,
         'name': 'Мтм-23',
         'leader': {'id': 3, 'name': 'Ігор Дорощук'}},
    )
    return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)