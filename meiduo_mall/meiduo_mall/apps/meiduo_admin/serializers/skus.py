from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from goods.models import SKUImage, SKU
from meiduo_mall.utils.fdfs.storage import FDFSStorage


class SKUImageSerializer(ModelSerializer):
    sku = serializers.StringRelatedField(label='SKU商品名称')
    sku_id = serializers.IntegerField(label='SKU商品ID')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')

    def validate_sku_id(self, value):
        # sku商品是否存在
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        return sku

    def create(self, validated_data):
        """sku商品上传图片保存"""
        # 获取上传图片
        file = validated_data['image']

        # 上传文件到FDFS系统
        fdfs = FDFSStorage()

        try:
            file_id = fdfs._save(file.name, file)
        except Exception:
            raise APIException('上传文件FDFS系统失败')

        # 保存上传图片记录
        file_id = file_id.replace('\\', '/')
        sku = validated_data['sku_id']

        sku_image = SKUImage.objects.create(
            sku=sku,
            image=file_id
        )

        # 如果sku商品没有默认图片，则设置其默认图片
        if not sku.default_image:
            sku.default_image = sku_image.image.url
            sku.save()

        return sku_image

    def update(self, instance, validated_data):
        '''sku上传图片修改'''
        file = validated_data['image']
        fdfs = FDFSStorage()
        try:
            file_id = fdfs.save(file.name, file)
        except Exception:
            raise APIException('上传文件FDFS系统失败')

        instance.image = file_id
        instance.save()

        return instance


class SKUSimpleSerializer(ModelSerializer):
    '''SKU商品序列化器'''
    class Meta:
        model = SKU
        fields = ('id', 'name')




