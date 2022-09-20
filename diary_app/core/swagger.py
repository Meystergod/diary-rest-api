from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title = 'Rest-like API',
        default_version = '1.0.0',
        description = 'Swagger API documentation',
    ),
    public = True,
)
