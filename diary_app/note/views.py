from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .serializers import NoteSerializer
from .filters import NotesFilter
from .models import Note
from .permissions import IsOwnerOrReadOnly
from .paginations import NoteAPIListPagination


class NoteAPIList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = NotesFilter

    pagination_class = NoteAPIListPagination

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Note.objects.all().exclude(Q(diary__kind = 'private') & ~Q(diary__user = self.request.user))


class NoteAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        return Note.objects.all().exclude(Q(diary__kind = 'private') & ~Q(diary__user = self.request.user))
