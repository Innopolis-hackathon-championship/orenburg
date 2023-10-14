from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.db.models import Q

from .. import models
from . import serializers


class TakeDeliveryView(APIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [AllowAny]

    def get(self, request: Request):
        serializer = self.serializer_class(
            models.ProductModel.objects.all(),
            many=True
        )
        
        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def post(self, request: Request):
        for product in request.data:
            instance = models.ProductModel.objects.get(pk=product["id"])
            
            serializer = self.serializer_class(
                instance, data=product
            )
            
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
        
        return Response({
            "message": "ok"
        }, status.HTTP_200_OK)


class NewOrdersView(generics.ListAPIView):
    queryset = models.OrderModel.objects.filter(
        status__in=["prepare", "ready"]
    )
    serializer_class = serializers.OrderSerializer
