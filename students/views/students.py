from django.shortcuts import render
from django.http import HttpResponse

# Views for Students
def students_list(request):
    students = (
       {'id': 1,
        'first_name': 'Дмитро',
        'last_name': 'Літвінов',
        'ticket': 212,
        'image': 'img/vlad.jpg'},
       {'id': 2,
        'first_name': 'Віталій',
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