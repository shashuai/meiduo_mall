from django.conf.urls import url
from meiduo_admin.views import users

urlpatterns = [
    # 进行url配置
    url(r'^authorizations/$', users.AdminAuthorizeView.as_view()),
]
