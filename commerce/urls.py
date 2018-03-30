from django.conf.urls import url
from commerce.views import WechatGroupView, SubscriptionView

urlpatterns = [
   url('wechatgroup', WechatGroupView.as_view()),
   url('subscription', SubscriptionView.as_view()),
]
