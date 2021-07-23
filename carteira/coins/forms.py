from django import forms
from django.db import models
from django.forms import fields

from .models import Coin

class CoinForm(forms.ModelForm):

    class Meta:
        model = Coin
        fields = ("nome", "valor", "modalidade")
