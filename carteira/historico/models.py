from django.db import models
from django.contrib.auth import get_user_model


class Coin(models.Model):

    STATUS = (
        ('aplicacao', 'Aplicação'),
        ('resgate', 'Resgate')
    )

    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    modalidade = models.CharField(max_length=9, choices=STATUS)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descricao
