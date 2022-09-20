from django.db import models
from django.utils.translation import gettext_lazy as _

from diary.models import Diary
from account.models import User


class Note(models.Model):
    content = models.TextField(_('content'))
    diary = models.ForeignKey(Diary, verbose_name = _('diary'), related_name = _('notes'), on_delete = models.CASCADE)

    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')
