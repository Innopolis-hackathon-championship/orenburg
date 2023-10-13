from django.urls import path

from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("take-delivery/", views.TakeDeliveryView.as_view, name="take_delivery")
]
