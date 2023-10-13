from django.urls import path, include


urlpatterns = [
    path("orders/", include("api.orders.urls")),
    path("", include("api.profiles.urls")),
    path("products/", include("api.products.urls")),
]
