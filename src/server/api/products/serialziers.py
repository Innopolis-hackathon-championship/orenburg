from rest_framework import serializers

from . import models


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = models.ProductModel
        fields = "__all__"
