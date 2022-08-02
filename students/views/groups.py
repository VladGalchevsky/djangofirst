from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _

from students.models import Group
from students.util import paginate


def groups_list(request):
    groups = Group.objects.all()

    # try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title',):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    # apply pagination, 2 groups per page
    context = paginate(groups, 2, request, {}, var_name='groups')

    return render(request, 'students/groups_list.html', context)


class GroupForm(ModelForm):

    class Meta:
        model = Group
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
            self.helper.form_action = reverse('groups_add')
        else:
            reverse_groups_edit = reverse('groups_edit',
                                          kwargs={'pk': kwargs['instance'].id})
            self.helper.form_action = reverse_groups_edit
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        if add_form:
            submit = Submit('add_button', _('Add'))
        else:
            submit = Submit('save_button', _('Save'))
        self.helper.layout.append(FormActions(
            submit,
            Submit('cancel_button', _('Cancel'), css_class='btn-danger'),
        ))


class BaseGroupFormView:

    def get_success_url(self):
        return '%s?status_message=%s' % (reverse('groups'),
                                         _("Changes saved successfully!"))

    def post(self, request, *args, **kwargs):
        # handle cancel button
        if request.POST.get('cancel_button'):
            return (
                HttpResponseRedirect(
                    reverse('groups') +
                    '?status_message=%s' % _("Changes canceled."))
            )
        else:
            return super().post(request, *args, **kwargs)


class GroupAddView(BaseGroupFormView, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'


class GroupUpdateView(BaseGroupFormView, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'


class GroupDeleteView(BaseGroupFormView, DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'
