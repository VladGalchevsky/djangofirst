from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Student, Group
from django.urls import reverse
from datetime import datetime
from django.views.generic import CreateView, DeleteView, UpdateView
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm


def students_list(request):
    students = Student.objects.all()

    # try to order students list

    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver
    # last page of results.
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', 
    {'students': students})


class StudentsForm(ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False

        # set form tag attributes
        if add_form:
            self.helper.form_action = reverse('students_add')
        else:
            reverse_students_edit = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})
            self.helper.form_action = reverse_students_edit
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        if add_form:
            submit = Submit('add_button', 'Додати')
        else:
            submit = Submit('save_button', 'Зберегти')
        self.helper.layout.append(FormActions(
            submit,
            Submit('cancel_button', 'Скасувати', css_class='btn-danger'),
        ))


class BaseStudentsFormView:

    def get_success_url(self):
        return '%s?status_message=Зміни успішно збережено!' \
               % reverse('home')

    def post(self, request, *args, **kwargs):
        # handle cancel button
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('home') +
                                        '?status_message=Зміни скасовано.')
        else:
            return super().post(request, *args, **kwargs)


class StudentsAddView(BaseStudentsFormView, CreateView):
    model = Student
    form_class = StudentsForm
    template_name = 'students/students_add.html'


class StudentsUpdateView(BaseStudentsFormView, UpdateView):
    model = Student
    form_class = StudentsForm
    template_name = 'students/students_edit.html'


class StudentsDeleteView(BaseStudentsFormView, DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'