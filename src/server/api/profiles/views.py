import random
import string

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http.request import HttpRequest

from . import serializers
from . import models


class UsersView(generics.ListCreateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.UserListSerializer
    
    def post(self, request: Request, *args, **kwargs):
        # Generate random code.
        code = random.sample(string.ascii_lowercase, 5)
        code = ''.join(code)
        # Extend json from body.
        request.data["code"] = code
        # Generate unverified user.
        return super().post(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.UserDetailSerializer

class UserCart(APIView):
    def get(request: Request, pk: int):
        user = get_object_or_404(models.UserModel, pk=pk)
        serializer = serializers.CartSerializer(user.cart, many=True)
        return Response(
            serializer.data,
            status.HTTP_200_OK
            )
    
    def post(request: Request, pk: int):
        data = request.data
        models.CartModel(
            user_id=pk,
            product_id=data["product_id"],
            quantity=data["quantity"]
        )
        

def verify(request: HttpRequest, pk: int):
    """User verifying endpoint"""
    user = get_object_or_404(models.UserModel, pk=pk)
    code = request.GET['code']
    if not user.verify(code):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)
