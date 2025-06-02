from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings
from users.manager import CustomUserManager


class CustomUser(AbstractUser):
    """Моделька для пользователя"""
    username = None
    phone_number = models.CharField(max_length=11,
                                    validators=[MinLengthValidator(6)],
                                    unique=True)
    balance = models.PositiveBigIntegerField(default=0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='отправленные_транзакции', default=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='полученные_транзакции', default=True)

    def __str__(self):
        return f"{self.sender.phone_number} → {self.recipient.phone_number}: {self.balance}"

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
