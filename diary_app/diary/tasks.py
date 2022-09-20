from celery import shared_task
from .models import Diary
from django.utils import timezone

@shared_task
def remove_old_diaries():
    Diary.objects.filter(kind='private').exclude(expiration=None).filter(expiration__lte=timezone.now()).delete()
