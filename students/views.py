from django.shortcuts import render
from django.http import HttpResponse

# Views for Students
def students_list(request):
    students = (
       {'id': 1,
        'first_name': 'Владислав',
        'last_name': 'Літвінов',
        'ticket': 212,
        'image': 'img/vlad.jpg'},
       {'id': 2,
        'first_name': 'Андрій',
        'last_name': 'Подоба',  
        'ticket': 213,
        'image': 'img/andrew.jpeg'},
       {'id': 3,
        'first_name': 'Ігор',
        'last_name': 'Дорощук',
        'ticket': 214,
        'image': 'img/igor.jpeg'}
    )
    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)


# Views for Groups
def groups_list(request):
    return HttpResponse('<h1>Groups Listing</h1>')

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

# Create your views here.
