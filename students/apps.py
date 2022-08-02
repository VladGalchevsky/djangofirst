from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StudentsConfig(AppConfig):
    name = 'students'
    verbose_name = _("Students Database")

    def ready(self):
        from students import signals
