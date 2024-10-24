from django.db import models


class Currency(models.TextChoices):
    MDL = 'MDL'
    EUR = 'EUR'


class Laptop(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    brand = models.CharField(max_length=255)
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.MDL
    )

    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'laptops'



