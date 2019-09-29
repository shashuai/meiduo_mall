from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SKUImage, SKU, GoodsCategory
from meiduo_admin.serializers.categories import CategorySimpleSerializer
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSerializer


class SKUImageViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_url_regex = '\d+'
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer


class SKUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUSimpleSerializer
    pagination_class = None



class SKUViewSet(ModelViewSet):
    '''SKU视图集'''
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    def get_queryset(self):
        '''获取当前视图所使用的查询集'''
        keyword = self.request.query_params.get('keyword')
        if keyword:
            skus = SKU.objects.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))
        else:
            skus = SKU.objects.all()

        return skus
    serializer_class = SKUSerializer



class SKUCategoriesView(ListAPIView):
    serializer_class = CategorySimpleSerializer

    def get_queryset(self):
        '''返回所有第三级分类'''
        categories = GoodsCategory.objects.filter(subs=None)

        return categories
    pagination_class = None


