from django.conf.urls import url
from account.views import LoginView, TokenView

urlpatterns = [
   url('login', LoginView.as_view()),
   url('token', TokenView.as_view()),
]
