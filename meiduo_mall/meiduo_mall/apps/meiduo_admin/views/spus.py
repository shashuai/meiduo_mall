from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from goods.models import SPU, SPUSpecification
from meiduo_admin.serializers.spus import SPUSimpleSerializer, SPUSpecSerializer


class SPUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SPU.objects.all()
    serializer_class = SPUSimpleSerializer

    pagination_class = None


class SPUSpecView(GenericAPIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        '''
        获取spu规格选项数据
        1. 根据pk获取spu specs数据
        2. 将spu数据序列化并返回
        '''
        specs = SPUSpecification.objects.filter(spu_id=pk)
        serializer = SPUSpecSerializer(specs, many=True)

        return Response(serializer.data)


# 上一个代码优化
# class SPUSpecView(ListAPIView):
#     permission_classes = [IsAdminUser]
#
#     # 指定序列化器类
#     serializer_class = SPUSpecSerializer
#
#     def get_queryset(self):
#         """返回视图所使用的查询集"""
#         # 获取pk
#         pk = self.kwargs['pk']
#         return SPUSpecification.objects.filter(spu_id=pk)
#
#     # 注：关闭分页
#     pagination_class = None