from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User


class Diary(models.Model):
    class Kind(models.TextChoices):
        PUBLIC = "public"
        PRIVATE = "private"

    kind = models.CharField(_('kind'), max_length = 64, choices = Kind.choices)
    title = models.CharField(_('title'), max_length = 256, unique = True)
    expiration = models.DateTimeField(_('expiration'), null = True, blank = True)
    user = models.ForeignKey(User, verbose_name = _('user'), related_name = _('diaries'), on_delete = models.CASCADE)

    class Meta:
        verbose_name = _('diary')
        verbose_name_plural = _('diaries')

    def __str__(self):
        return self.title
