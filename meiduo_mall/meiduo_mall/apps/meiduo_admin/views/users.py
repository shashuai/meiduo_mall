from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_admin.serializers.users import AdminAuthSerializer


# class AdminAuthorizeView(GenericAPIView):
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
