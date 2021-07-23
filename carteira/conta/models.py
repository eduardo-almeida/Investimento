from django.db import models
from django.contrib.auth import get_user_model


class Conta(models.Model):

    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

