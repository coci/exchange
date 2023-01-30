from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserBalance(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	balance = models.IntegerField(default=0)

	@receiver(post_save, sender=User)
	def create_user_balance(sender, instance, created=False, **kwargs):
		if created:
			UserBalance.objects.create(
				user=instance,
			)
