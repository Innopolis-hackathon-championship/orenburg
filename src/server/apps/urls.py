from django.urls import path, include


urlpatterns = [
    path("", include("apps.core.urls")),
    path("api/", include("apps.core.api.urls")),
]
