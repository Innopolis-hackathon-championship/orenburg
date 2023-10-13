from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings

from . import serializers
from . import models


class UsersView(generics.ListCreateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.UserListSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.UserDetailSerializer
