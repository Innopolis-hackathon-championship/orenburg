from django.urls import path

from . import views


urlpatterns = [
    path("order/test/", views.TestView.as_view(), name="test")
]
