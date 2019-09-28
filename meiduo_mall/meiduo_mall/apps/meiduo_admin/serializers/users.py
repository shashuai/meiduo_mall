import re

from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.models import User


class AdminAuthSerializer(ModelSerializer):
    '''管理员序列化器类'''
    username = serializers.CharField(label='用户名')
    token = serializers.CharField(label='JWT Token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        try:
            user = User.objects.get(username=username, is_staff=True)
            print(user.password)
        except User.DoesNotExit:
            raise serializers.ValidationError('用户名或密码错误')
        else:
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或密码错误')
            attrs['user'] = user
        return attrs


    def create(self, validated_data):
        user = validated_data['user']
        user.last_login = timezone.now()
        user.save()

        from rest_framework_jwt.settings import api_settings
        # 组织payload数据的方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成jwt token数据的方法
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 组织payload数据
        payload = jwt_payload_handler(user)
        # 生成jwt token
        token = jwt_encode_handler(payload)
        user.token = token

        return user


class UserSerializer(ModelSerializer):
    '''用户序列化器类'''
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'password')
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户名最小长度为5',
                    'max_length': '用户名最大长度为20'
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '密码最小长度为8',
                    'max_length': '密码最大长度为20'
                }
            }
        }


    def validate_mobile(self, value):
        '''手机号格式, 手机号是否注册'''
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号码格式不正确')

        res = User.objects.filter(mobile=value).count()
        if res > 0:
            raise serializers.ValidationError('手机号已经注册')

        return value


    def create(self, validated_data):
        '''创建并保存新用户数据'''
        user = User.objects.create_user(**validated_data)

        return user
