from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.base import Model

from coins.models import Coin

class Task(models.Model):

    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)    
    quantidade = models.IntegerField()
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coin.nome

    def total(self):
        return self.quantidade * self.coin.valor  

