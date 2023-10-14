from django.urls import path

from . import views


urlpatterns = [
    path("take-delivery/", views.TakeDeliveryView.as_view(), name="api__take_delivery"),
    path("new-orders/", views.NewOrdersView.as_view(), name="api__new_orders")
]
