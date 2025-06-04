from django.contrib import admin
from django.urls import path

from bank.views import UserBalanceAPIView, UserSearchAPIView, \
    ClickButtonAPIView, SendMoneyAPIView, TransactionHistoryAPIView
from users.views import UserRegisterAPIView, UserLoginAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/register/', UserRegisterAPIView.as_view()), # эдпоинт для регистрации
    path('api/v1/users/login/', UserLoginAPIView.as_view()),       # эдпоинт для логина
    path('api/v1/user/balance/', UserBalanceAPIView.as_view()),    # эдпоинт для баланса
    path('api/v1/user/search/', UserSearchAPIView.as_view()),      # эдпоинт для поиска
    path('api/v1/user/click-button/', ClickButtonAPIView.as_view()),     # эдпоинт для кнопки увеличение баланса
    path('api/v1/user/send-money/', SendMoneyAPIView.as_view()),         # эдпоинт для оправки денег другому пользователю
    path('api/v1/user/history/', TransactionHistoryAPIView.as_view()),   # эдпоинт для просмотра истории транзакции
]
