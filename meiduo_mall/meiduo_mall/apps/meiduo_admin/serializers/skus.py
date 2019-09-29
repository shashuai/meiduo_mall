from django.db import transaction
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from goods.models import SKUImage, SKU, SKUSpecification, GoodsCategory, SPU, SpecificationOption
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


class SKUSpecSerializer(serializers.ModelSerializer):
    """商品规格信息序列化器类"""
    spec_id = serializers.IntegerField(label='规格id')
    option_id = serializers.IntegerField(label='选项id')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""
    # 关联对象嵌套序列化
    spu = serializers.StringRelatedField(label='SPU名称')
    category = serializers.StringRelatedField(label='三级分类名称')

    spu_id = serializers.IntegerField(label='SPU编号')
    category_id = serializers.IntegerField(label='三级分类ID')

    # 关联对象嵌套序列化
    specs = SKUSpecSerializer(label='商品规格信息', many=True)

    class Meta:
        model = SKU
        # 排除模型的字段
        exclude = ('create_time', 'update_time', 'default_image')

    def validate(self, attrs):
        category_id = attrs['category_id']
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('分类不存在')

        spu_id = attrs['spu_id']
        try:
            spu = SPU.objects.get(id=spu_id)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('SPU商品不存在')

        if spu.category3_id != category_id:
            raise serializers.ValidationError('SPU分类信息错误')

        spu_specs = spu.specs.all()
        spec_count = spu_specs.count()
        specs = attrs['specs']

        if spec_count > len(specs):
            raise serializers.ValidationError('SKU规格数据不完整')

        spu_specs_ids = [spec.id for spec in spu_specs]
        specs_ids = [spec.get('spec_id') for spec in specs]

        if spu_specs_ids.sort() != specs_ids.sort():
            raise serializers.ValidationError('商品规格数据有误')

        for spec in specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')

            options = SpecificationOption.objects.filter(spec_id=spec_id)
            option_ids = [option.id for option in options]
            if option_id not in option_ids:
                raise serializers.ValidationError('规格选项数据有误')

        return attrs

    def create(self, validated_data):
        '''保存sku商品数据'''
        specs = validated_data.pop('specs')

        with transaction.atomic():
            # 调用父类方法新增sku商品
            sku = super().create(validated_data)

            # 保存商品规格信息
            for spec in specs:
                SKUSpecification.objects.create(
                    sku=sku,
                    spec_id=spec.get('spec_id'),
                    option_id=spec.get('option_id')
                )
        return sku

    def update(self, instance, validated_data):
        '''修改sku商品数据'''
        specs = validated_data.pop('specs')
        sku_specs = [{
            'spec_id': spec.spec_id,
            'option_id': spec.option_id
        } for spec in instance.specs.all()]
        with transaction.atomic():
            # 调用父类方法更新sku商品
            sku = super().update(instance, validated_data)

            # 保存商品规格信息
            if specs != sku_specs:
                # 清除sku原有的规格信息
                instance.specs.all().delete()

                for spec in specs:
                    SKUSpecification.objects.create(
                        sku=instance,
                        spec_id=spec.get('spec_id'),
                        option_id=spec.get('option_id')
                    )

        # 当新增sku商品信息之后，异步生成对应商品的静态详情页面
        # from celery_tasks.html.tasks import generate_static_sku_detail_html
        # generate_static_sku_detail_html.delay(sku.id)

        return sku
