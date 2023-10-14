from django.urls import path

from . import views


urlpatterns = [
    path("take-delivery/", views.TakeDeliveryView.as_view(), name="api__take_delivery"),
    path("new-orders/", views.NewOrdersView.as_view(), name="api__new_orders"),
    
    path("delivery/find/", views.FindDeliveryView.as_view(), name="api__find_delivery"),
    path("delivery/take/", views.TakeReadyDeliveryView.as_view(), name="api__give_delivery"),
    path("delivery/give/", views.GiveDeliveryView.as_view(), name="api__give_delivery"),
    path("delivery/status/", views.DeliveryStatusView.as_view(), name="api__status_delivery"),
    path("delivery/arrived/", views.DeliveryArrivedView.as_view(), name="api__status_delivery"),
    
    path("order/ready/", views.OrderReadyView.as_view(), name="api__order_ready"),
    path("order/take/", views.OrderTakeView.as_view(), name="api__order_take")
]
