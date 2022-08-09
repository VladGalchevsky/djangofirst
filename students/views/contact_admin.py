import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    from_email = forms.EmailField(
        label=_("Your Email Address"))

    subject = forms.CharField(
        label=_("Email Subject"),
        max_length=128)

    message = forms.CharField(
        label=_(u"Email Body"),
        widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        # call original initializator
        super().__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper(self)

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', _('Send')))


@permission_required('auth.add_user', raise_exception=True)
def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)

        # check whether user data is valid:
        if form.is_valid():
            # send email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [settings.ADMIN_EMAIL])
            except Exception:
                message = _("An error occurred during email transfer. Please, "
                            "try again later.")
                logger = logging.getLogger(__name__)
                logger.exception(message)
            else:
                message = _("Message sent successfully!")

            # redirect to same contact page with success message
            return HttpResponseRedirect(
                '%s?status_message=%s' % (reverse('contact_admin'), message))

    # if there was not POST render blank form
    else:
        form = ContactForm()

    return render(request, 'contact_admin/form.html', {'form': form})