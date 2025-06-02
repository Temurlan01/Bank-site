from django.contrib import admin
from django.urls import path

from bank.views import UserBalanceAPIView, UserSearchAPIView, \
    ClickButtonAPIView, SendMoneyAPIView
from users.views import UserRegisterAPIView, UserLoginAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/register/', UserRegisterAPIView.as_view()),
    path('api/v1/users/login/', UserLoginAPIView.as_view()),
    path('api/v1/user/balance/', UserBalanceAPIView.as_view()),
    path('api/v1/user/search/', UserSearchAPIView.as_view()),
    path('api/v1/user/button/', ClickButtonAPIView.as_view()),
    path('api/v1/user/send/', SendMoneyAPIView.as_view()),
]
