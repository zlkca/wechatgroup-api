from django.conf.urls import url
from commerce.views import WechatGroupListView, WechatGroupFormView, CategoryListView, CategoryFormView, QRListView, SubscriptionView

urlpatterns = [
    url('categories', CategoryListView.as_view()),
    url('category/(?P<id>[0-9]+)', CategoryFormView.as_view()),
    url('category', CategoryFormView.as_view()),
    url('wechatgroup/(?P<id>[0-9]+)', WechatGroupFormView.as_view()),
    url('wechatgroups', WechatGroupListView.as_view()),
    url('wechatgroup', WechatGroupFormView.as_view()),
    url('qr', QRListView.as_view()),
    url('subscription', SubscriptionView.as_view()),
]
