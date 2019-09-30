from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from meiduo_admin.serializers.orders import OrderListSerializer, OrderDetailSerializer, OrderStatusSerializer
from orders.models import OrderInfo


class OrdersViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    # serializer_class = OrderListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        else:
            return OrderDetailSerializer
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if not keyword:
            return OrderInfo.objects.all()

        else:
            return OrderInfo.objects.filter(skus__sku__name__contains=keyword)

    def status(self, request, pk):
        '''
        修改订单状态
        1. 校验订单是否有效
        2. 获取订单状态status并校验(status必传, status是否合法)
        3. 修改并保存订单的状态
        4. 返回应答
        '''
        order = self.get_object()
        serializer = OrderStatusSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


