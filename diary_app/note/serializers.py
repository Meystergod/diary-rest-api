from rest_framework import serializers
from diary.models import Diary
from django.utils.translation import gettext_lazy as _

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('content', 'diary',)

    def validate(self, data):
        queryset = Diary.objects.all().filter(user = self.context['request'].user)
        if data['diary'] not in queryset:
            raise serializers.ValidationError({'diary': _('The note cannot be created for another user.')})
        
        return data
