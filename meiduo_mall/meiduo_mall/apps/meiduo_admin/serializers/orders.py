from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


class OrderListSerializer(ModelSerializer):
    '''订单序列化器类'''
    create_time = serializers.DateTimeField(format='%Y-%m-%d:%H-%M-%S')
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'create_time')

class SKUSimpleSerializer(ModelSerializer):
    '''订单商品序列化器类'''
    class Meta:
        model = SKU
        fields = ('name', 'default_image')

class OrderSKUSerializer(ModelSerializer):
    sku = SKUSimpleSerializer(label='SKU商品')
    class Meta:
        model = OrderGoods
        fields = ('count', 'price', 'sku')

class OrderDetailSerializer(ModelSerializer):
    '''顶顶那详情序列化器类'''
    user = serializers.StringRelatedField(label='下单用户')
    skus = OrderSKUSerializer(label='订单商品', many=True)
    create_time = serializers.DateTimeField(label='下单时间', format='%Y-%m-%d:%H-%M-%S')
    class Meta:
        model = OrderInfo
        exclude = ('update_time', 'address')


class OrderStatusSerializer(ModelSerializer):
    '''订单状态序列化器类'''
    model = OrderInfo
    fields = ('order_id', 'status')
    read_only_fields = ('order_id', )