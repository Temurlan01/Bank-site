from django.db import models
from users.models import CustomUser


class Transaction(models.Model):
    """Вью для транзакций"""
    sender = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='sent_transactions'
                               )
    recipient = models.ForeignKey(CustomUser,
                                  on_delete=models.CASCADE,
                                  related_name='received_transactions'
                                  )
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)