from django_filters import rest_framework

from .models import Diary


class DiaryFilter(rest_framework.FilterSet):
    class Meta:
        model = Diary
        fields = ['user_id']
