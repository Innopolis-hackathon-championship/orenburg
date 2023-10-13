from rest_framework import serializers

from . import models
from api.products.models import ProductDetailSerializer

class UserListSerializer(serializers.ModelSerializer):
    balance = serializers.IntegerField(read_only=True)
    role = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.UserModel
        fields = (
            "pk", "username", "fullname", "telegram_id", "balance", "role", "date_joined"
        )


class UserDetailSerializer(serializers.ModelSerializer):
    username = serializers.IntegerField(read_only=True)
    telegram_id = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.UserModel
        fields = (
            "pk", "username", "fullname", "telegram_id", "balance", "role", "date_joined"
        )


class CartSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()
    class Meta:
        model = models.CartModel
        fields = (
            "product",
            "quantity",
        )
