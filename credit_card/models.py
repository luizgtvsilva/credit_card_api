from django.db import models
from django.core.validators import MinLengthValidator


class Holder(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2)])


class CreditCard(models.Model):
    exp_date = models.DateField()
    number = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)
    holder = models.ForeignKey(Holder, on_delete=models.CASCADE)