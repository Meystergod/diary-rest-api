from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .serializers import DiarySerializer
from .filters import DiaryFilter
from .models import Diary
from .permissions import IsOwnerOrReadOnly
from .paginations import DiaryAPIListPagination


class DiaryAPIList(generics.ListCreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = DiaryFilter

    pagination_class = DiaryAPIListPagination

    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class DiaryAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer

    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)
