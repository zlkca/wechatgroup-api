from django.conf.urls import url
from account.views import LoginView, TokenView, UserView

urlpatterns = [
   url('login', LoginView.as_view()),
   url('token', TokenView.as_view()),
   url('user', UserView.as_view()),
]
