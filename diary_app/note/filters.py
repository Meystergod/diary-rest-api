from django_filters import rest_framework

from .models import Note


class NotesFilter(rest_framework.FilterSet):
    class Meta:
        model = Note
        fields = ['diary_id']
