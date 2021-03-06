from rest_framework import serializers

from goods.models import GoodsCategory


class CategorySimpleSerializer(serializers.ModelSerializer):
    """分类序列化器类"""
    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')