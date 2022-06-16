from django.shortcuts import render
from django.http import HttpResponse

def journal_list(request):
    return render(request, 'students/journal_list.html', {})

def journal_jid(request, jid):
    return HttpResponse(f'<h1>journal of visits to a particular student {jid}</h1>')

def journal_update(request):
    return HttpResponse('<h1>Journal update</h1>')
