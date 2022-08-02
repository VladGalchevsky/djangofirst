from django.db import models
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    """Group Model"""

    title = models.CharField(
        max_length=256,
        verbose_name=_("Title"))

    leader = models.OneToOneField(
        'Student',
        verbose_name=_("Leader"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    notes = models.TextField(
        blank=True,
        verbose_name=_("Extra Notes"))

    class Meta(object):
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self):
        if self.leader:
            return "%s (%s %s)" % (self.title, self.leader.first_name,
                                   self.leader.last_name)
        else:
            return "%s" % (self.title,)
