from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserListSerializer, UserDetailSerializer
from .paginations import UserAPIListPagination


class UserAPIList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    pagination_class = UserAPIListPagination

    permission_classes = (AllowAny,)


class UserAPIDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    permission_classes = (IsAuthenticated,)
