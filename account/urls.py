from django.conf.urls import url
from account.views import UserView

urlpatterns = [
   url('user', UserView.as_view()),
]
