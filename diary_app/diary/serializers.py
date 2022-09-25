from rest_framework import serializers

from .models import Diary


class DiarySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.id')

    class Meta:
        model = Diary
        fields = ('id', 'title', 'kind', 'expiration', 'user')
