from django.db import models
from django.contrib.auth import get_user_model

from django.urls import reverse

class Coin(models.Model):

    STATUS = (
        ('fixa', 'Renda Fixa'),
        ('variavel', 'Renda Variável'),
        ('cripto', 'Cripto')
    )

    nome = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    modalidade = models.CharField(max_length=8, choices=STATUS)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ("nome",)
        verbose_name = "ativo"
        verbose_name_plural = "ativos"

    def get_absolute_url(self):
        return reverse("products:list_by_category", kwargs={"slug": self.slug})
