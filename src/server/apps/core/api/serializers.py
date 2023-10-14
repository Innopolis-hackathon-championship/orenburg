from rest_framework import serializers

from .. import models


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    
    class Meta:
        model = models.ProductModel
        fields = "__all__"
        

class OrderToProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = models.OrderToProductModel
        fields = ("product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = models.OrderModel
        fields = "__all__"

    def get_products(self, obj):
        return OrderToProductSerializer(
            models.OrderToProductModel.objects.filter(
                order=obj
            ),
            many=True
        ).data
