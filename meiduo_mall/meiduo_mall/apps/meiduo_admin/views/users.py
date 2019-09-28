from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_admin.serializers.users import AdminAuthSerializer, UserSerializer

# class AdminAuthorizeView(GenericAPIView):
from users.models import User


class AdminAuthorizeView(APIView):
    # serializer_class = AdminAuthSerializer
    def post(self, request):
        '''
        管理员登录:
        1. 获取参数并进行校验
        2. 服务器签发jwt token 数据
        3. 返回应答
        '''
        serializer = AdminAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)



# class UserInfoView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request):
#         """
#         获取普通用户数据:
#         1. 获取keyword关键字
#         2. 查询普通用户数据
#         3. 将用户数据序列化并返回
#         """
#         keyword = request.query_params.get('keyword')
#         if keyword is None or keyword == '':
#             user = User.objects.filter(is_staff=False)
#         else:
#             user = User.objects.filter(is_staff=False, username__contains=keyword)
#
#         serializer = UserSerializer(user, many=True)
#         return Response(serializer.data)


# 代码优化
# class UserInfoView(GenericAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         keyword = self.request.query_params.get('keyword')
#         if keyword is None or keyword == '':
#             users = User.objects.filter(is_staff=False)
#         else:
#             users = User.objects.filter(is_staff=False, username__contains=keyword)
#
#         return users
#
#     def get(self, request):
#         """
#         获取普通用户数据:
#         1. 获取keyword关键字
#         2. 查询普通用户数据
#         3. 将用户数据序列化并返回
#         """
#         users = self.get_queryset()
#         serializer = self.get_serializer(users, many=True)
#         return Response(serializer.data)


# 最后优化
# class UserInfoView(ListAPIView):
#     permission_classes = [IsAdminUser]
#     # 指定视图所使用的序列化器类
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         """返回视图所使用的查询集"""
#         # 1. 获取keyword关键字
#         keyword = self.request.query_params.get('keyword')
#
#         # 2. 查询普通用户数据
#         if keyword is None or keyword == '':
#             users = User.objects.filter(is_staff=False)
#         else:
#             users = User.objects.filter(is_staff=False, username__contains=keyword)

        # return users


    # def post(self, request):
    #     """
    #     新增用户数据:
    #     1. 获取参数并进行校验
    #     2. 创建并保存新用户数据
    #     3. 将新用户数据序列化并返回
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# 合并两个函数
class UserInfoView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    # 指定视图所使用的序列化器类
    serializer_class = UserSerializer

    def get_queryset(self):
        """返回视图所使用的查询集"""
        # 1. 获取keyword关键字
        keyword = self.request.query_params.get('keyword')

        # 2. 查询普通用户数据
        if keyword is None or keyword == '':
            users = User.objects.filter(is_staff=False)
        else:
            users = User.objects.filter(is_staff=False, username__contains=keyword)

        return users
