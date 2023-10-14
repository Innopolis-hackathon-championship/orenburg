from django.urls import path, include


urlpatterns = [
    path("", include("api.orders.urls")),
    path("", include("api.profiles.urls")),
    path("", include("api.products.urls")),
]
