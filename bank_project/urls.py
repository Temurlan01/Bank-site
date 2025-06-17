from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from bank.views import UserBalanceAPIView, UserSearchAPIView, \
    ClickButtonAPIView, SendMoneyAPIView, TransactionHistoryAPIView
from users.views import UserRegisterAPIView, UserLoginAPIView


schema_view = get_schema_view(
   openapi.Info(
      title="Бэкенд документация API для Банк сайта",
      default_version='v1',
      description="API предоставляет возможность зарегистрироваться, логиниться, поиск других пользователей, кнопка для увеличение баланса, отправка денег другим пользователям, просмотр истории ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="temur07lan@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('', lambda request: redirect('/api/v1/users/register/')),
    path('admin/', admin.site.urls),
    path('api/v1/users/register/', UserRegisterAPIView.as_view()),             # эдпоинт для регистрации
    path('api/v1/users/login/', UserLoginAPIView.as_view()),                   # эдпоинт для логина
    path('api/v1/user/balance-info/', UserBalanceAPIView.as_view()),           # эдпоинт для баланса
    path('api/v1/user/search-user/', UserSearchAPIView.as_view()),             # эдпоинт для поиска
    path('api/v1/user/increase-balance/', ClickButtonAPIView.as_view()),       # эдпоинт для кнопки увеличение баланса
    path('api/v1/user/send-money/', SendMoneyAPIView.as_view()),               # эдпоинт для оправки денег другому пользователю
    path('api/v1/user/transactions/', TransactionHistoryAPIView.as_view()),    # эдпоинт для просмотра истории транзакции
]
