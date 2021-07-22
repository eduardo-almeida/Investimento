from django.db import models

class Task(models.Model):

    STATUS = (
        ('renda fixa', 'renda fixa'),
        ('renda variável', 'renda variável'),
        ('cripto', 'cripto')
    )

    nome = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    modalidade = models.CharField(max_length=14, choices=STATUS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome