from django.urls import path

from . import views


urlpatterns = [
    path("users/", views.UsersView.as_view(), name="users"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="users-detail"),
    path("users/<int:pk>/virify", views.verify)
]
