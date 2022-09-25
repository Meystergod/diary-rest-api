from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Diary


class DiarySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.id')

    class Meta:
        model = Diary
        fields = ('id', 'title', 'kind', 'expiration', 'user')

    def validate(self, data):
        if data['kind'] == 'public' and data['expiration'] is not None:
            raise serializers.ValidationError({'expiration': _('The expiration date cannot be set for public diary.')})
        return data
