from django.contrib import admin
from django.urls import path
from diary.views import DiaryAPIDetail, DiaryAPIList
from note.views import NoteAPIList, NoteAPIDetail
from account.views import UserAPIList, UserAPIDetail
from .swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/user_list/', UserAPIList.as_view(), name = 'user-list'),
    path('api/v1/user/<int:pk>/detail/', UserAPIDetail.as_view(), name = 'user-detail'),

    path('api/v1/diary_list/', DiaryAPIList.as_view(), name = 'diary-list'),
    path('api/v1/diary/<int:pk>/detail/', DiaryAPIDetail.as_view(), name = 'diary-detail'),

    path('api/v1/note_list/', NoteAPIList.as_view(), name = 'note-list'),
    path('api/v1/note/<int:pk>/detail/', NoteAPIDetail.as_view(), name = 'note-detail'),

    path('api/v1/swagger/schema/', schema_view.with_ui('swagger', cache_timeout = 0), name = 'swagger-schema'),
]
