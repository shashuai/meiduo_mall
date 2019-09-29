from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from goods.models import SPU, SpecificationOption, SPUSpecification, SKU, GoodsCategory, SKUSpecification
from meiduo_admin.serializers.skus import SKUSpecSerializer


class SPUSimpleSerializer(ModelSerializer):
    """SPU序列化器类"""
    class Meta:
        model = SPU
        fields = ('id', 'name')


class SpecOptionSerializer(ModelSerializer):
    '''SPU规格序列化器类'''
    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')


class SPUSpecSerializer(ModelSerializer):
    '''SPU序列化器类'''
    spu = serializers.StringRelatedField(label='SPU名称')
    spu_id = serializers.IntegerField(label='SPU ID')

    options = SpecOptionSerializer(label='Opt选项', many=True)

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id', 'options')



