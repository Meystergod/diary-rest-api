from rest_framework import serializers

from .models import User


class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length = 8, write_only = True)
    diaries = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'diaries',)

    def create(self, validated_data):
        user = super(UserListSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    diaries = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    class Meta:
        model = User
        fields = ('id', 'email', 'date_joined', 'last_login', 'diaries')
