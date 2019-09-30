from django.conf.urls import url
from meiduo_admin.views import users, statistical, channels, skus, spus, orders
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # 进行url配置
    url(r'^authorizations/$', users.AdminAuthorizeView.as_view()),
    url(r'^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_increment/$', statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_active/$', statistical.UserActiveAcountView.as_view()),
    url(r'^statistical/day_orders/$', statistical.UserOrderCountView.as_view()),
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),
    url(r'^users/$', users.UserInfoView.as_view()),
    url(r'^goods/channel_types/$', channels.ChannelTypesView.as_view()),
    url(r'^goods/categories/$', channels.ChannelCategoriesView.as_view()),
    url(r'^skus/simple/$', skus.SKUSimpleView.as_view()),
    url(r'^skus/categories/$', skus.SKUCategoriesView.as_view()),
    url(r'^goods/simple/$', spus.SPUSimpleView.as_view()),
    url(r'^goods/(?P<pk>\d+)/specs/$', spus.SPUSpecView.as_view()),

]

router = DefaultRouter()
router.register('goods/channels', channels.ChannelViewSet, base_name='channels')
urlpatterns += router.urls

# 图片管理
router = DefaultRouter()
router.register(r'skus/images', skus.SKUImageViewSet, base_name='images')
urlpatterns += router.urls

# SKU商品管理
router = DefaultRouter()
router.register('skus', skus.SKUViewSet, base_name='skus')
urlpatterns += router.urls

# 订单管理
router = DefaultRouter()
router.register('orders', orders.OrdersViewSet, base_name='orders')
urlpatterns += router.urls