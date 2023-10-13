from django.urls import path, include


urlpatterns = [
    path("orders/", include("api.orders.urls")),
    path("profiles/", include("api.profiles.urls")),
    path("products/", include("api.products.urls")),
]
