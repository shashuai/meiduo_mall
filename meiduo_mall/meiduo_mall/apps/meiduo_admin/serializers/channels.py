from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory


class ChannelSerializer(ModelSerializer):
    category = serializers.StringRelatedField(label='一级分类名称')
    category_id = serializers.IntegerField(label='一级分类ID')

    group = serializers.StringRelatedField(label='频道组名称')
    group_id = serializers.IntegerField(label='频道组ID')

    class Meta:
        model = GoodsChannel
        exclude = ('create_time', 'update_time')

    def validate_category_id(self, value):
        try:
            GoodsCategory.objects.get(id=value, parent=None)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('一级分类不存在')

        return value

    def validate_group_id(self, value):
        try:
            GoodsChannelGroup.objects.get(id=value)
        except GoodsChannelGroup.DoesNotExist:
            raise serializers.ValidationError('频道组不存在')

        return value


class ChannelGroupSerializer(ModelSerializer):
    '''频道组序列化器类'''

    class Meta:
        model = GoodsChannelGroup
        fields = ('id', 'name')


class CategorySimpleSerializer(ModelSerializer):
    '''商品分类序列化器类'''

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')
