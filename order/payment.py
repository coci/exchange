from order.models import Order
from user_balance.models import UserBalance


class Payment:
	def __init__(self, user, coin, amount, coin_price, order_limit):
		self.user = user
		self.coin = coin
		self.amount = amount
		self.coin_price = coin_price
		self.order_limit = order_limit
		self.total_price = self.amount * self.coin_price
		self.user_balance = UserBalance.objects.get(user=self.user)

	def is_user_have_balance(self):
		if self.user_balance.balance >= self.total_price:
			return True
		else:
			return False

	def decrease_user_balance(self):
		self.user_balance.balance -= self.total_price
		self.user_balance.save()

	def is_total_price_allowed(self):
		if self.total_price >= self.order_limit:
			return True
		else:
			return False

	def create_database_record(self, status):
		order = Order.objects.create(
			user=self.user,
			coin=self.coin,
			coin_amount=self.amount,
			order_price=self.total_price,
			status=status
		)
		return order
