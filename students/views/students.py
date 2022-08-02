from datetime import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, UpdateView

from ..models import Group, Student
from ..util import get_current_group, paginate


def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # apply pagination, 3 students per page
    context = paginate(students, 3, request, {}, var_name='students')

    return render(request, 'students/students_list.html', context)


def students_add(request):
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            # errors collection
            errors = {}

            # data for student object
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = _("First Name field is required")
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = _("Last Name field is required")
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = _("Birthday field is required")
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = \
                        _("Please, enter correct date format "
                          "(e.g. 1984-12-30)")
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = _("Ticket number is required")
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = _("Please, select group")
            else:
                group = Group.objects.filter(pk=student_group).first()
                if group:
                    data['student_group'] = group
                else:
                    errors['student_group'] = _("Please, select correct group")

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo

            # save student
            if not errors:
                student = Student(**data)
                student.save()

                # redirect to students list
                return HttpResponseRedirect(
                    '%s?status_message=%s' %
                    (reverse('home'), _("Student added successfully!")))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(
                '%s?status_message=%s' %
                (reverse('home'), _("Student addition canceled!")))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
                      {'groups': Group.objects.all().order_by('title')})


class StudentUpdateForm(ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-3 col-form-label'
        self.helper.field_class = 'col-sm-9'

        # add buttons
        self.helper.layout.append(FormActions(
            Submit('add_button', _('Save')),
            Submit('cancel_button', _('Cancel'), css_class='btn-danger'),
        ))


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return '%s?status_message=%s' % (reverse('home'),
                                         _("Student updated successfully!"))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                '%s?status_message=%s' % (reverse('home'),
                                          _("Student update canceled!")))
        else:
            return super().post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return '%s?status_message=%s' % (reverse('home'),
                                         _("Student deleted successfully!"))
