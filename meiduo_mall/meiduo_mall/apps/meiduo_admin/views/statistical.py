from datetime import timedelta

from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import GoodsVisitCount
from meiduo_admin.serializers.statistical import GoodsVisitSerializer
from users.models import User


class UserTotalCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        获取网站总用户数
        1. 获取网站总用户数量
        2. 返回应答
        '''
        now_date = timezone.now()
        count = User.objects.count()
        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


class UserDayCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        获取日增用户数量
        1. 获取日增用户数量
        2. 返回应答
        '''
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(date_join__gte=now_date).count()

        response_data = {
            'data': now_date.date(),
            'count': count
        }
        return Response(response_data)


class UserActiveAcountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        获取日货用户量
        1. 获取日活用户量
        2. 返回应答
        '''
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_date).count()
        response_data =  {
            'date': now_date,
            'count': count
        }

        return Response(response_data)


class UserOrderCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        获取日下单用户数量
        1. 获取日下单用户数量
        2. 返回应答
        '''
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(orders__create_time__gte=now_date).count()

        response_data = {
            'date': now_date,
            'count': count
        }

        return Response(response_data)


class UserMonthCountView(APIView):
    '''
    获取当月每日新增用户数据
    1. 获取当月每日新增用户数据
    2. 返回应答
    '''
    def get(self, request):
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        begin_date = now_date - timedelta(days=29)

        count_list = []
        for i in range(30):
            cur_date = begin_date + timedelta(days=i)
            next_date = cur_date + timedelta(days=1)
            count = User.objects.filter(date_joined__lt=next_date).count()
            count_list.append({
                'date': cur_date.date(),
                'count': count
            })

        return Response(count_list)


class GoodsDayView(APIView):
    '''
    获取当日分类商品访问量
    1. 查询当日分类商品访问量
    2. 将查询到数据序列化返回
    '''
    def get(self, request):
        now_date = timezone.now().date()

        goods_visit = GoodsVisitCount.objects.filter(date=now_date)

        # 2. 将查询数据序列化并返回
        serializer = GoodsVisitSerializer(goods_visit, many=True)

        return Response(serializer.data)
