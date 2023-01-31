from django.contrib.auth.models import User
from django.db import models


class OrderStatus(models.TextChoices):
	success = 'success'
	pending = 'pending'


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	coin = models.CharField(max_length=50)
	coin_amount = models.IntegerField()
	order_price = models.IntegerField()
	status = models.CharField(max_length=20, choices=OrderStatus.choices)
