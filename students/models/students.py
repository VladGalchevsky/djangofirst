from django.db import models
from django.utils.translation import gettext_lazy as _


class Student(models.Model):
    """Student Model"""

    student_group = models.ForeignKey(
        'Group',
        verbose_name=_("Group"),
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_("First Name"))

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_("Last Name"))

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_("Middle Name"),
        default='')

    birthday = models.DateField(
        blank=False,
        verbose_name=_("Birthday"),
        null=True)

    photo = models.ImageField(
        blank=True,
        verbose_name=_("Photo"),
        null=True)

    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_("Ticket"))

    notes = models.TextField(
        blank=True,
        verbose_name=_("Extra Notes"))

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
