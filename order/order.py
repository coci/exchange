from pickle import loads, dumps

import redis

from order.exchange import ExchangeHandler
from order.models import Order, OrderStatus
from .env import REDIS_DB, REDIS_HOST, ORDER_LIMIT


class RedisHandler:
	def __init__(self):
		self.redis_connection = redis.Redis(host=REDIS_HOST, db=REDIS_DB)

	def get(self, coin):
		if self.redis_connection.get(coin):
			return loads(self.redis_connection.get(coin))
		else:
			return None

	def set(self, coin, data):
		self.redis_connection.set(coin, dumps(data))

	def remove(self, coin):
		self.redis_connection.delete(coin)


class PendingOrderHandler:

	def __init__(self, coin, amount, coin_price, order_id, cache):
		self.coin = coin
		self.amount = amount
		self.coin_price = coin_price
		self.total_price = self.amount * self.coin_price
		self.order_id = order_id
		self.cache = cache()

	def set_pending_order(self):
		"""
			cache/store pending order in redis
			format of redis will be something like this :

			"ABAN" : [{'1':5,'2':5},10,3]
			"AZAR" : [{'3':5,'7':5},10,3]

			as key i stored pair and for value i stored array which first of element are the hash map of-
			orders id with proper value ( coin amount * coin price ) and the second element are the sum of-
			all pending order in this pair and for the third element i stored coin amounts.

		"""

		if self.cache.get(self.coin):
			pending_order, total_sum, orders_amount = self.cache.get(self.coin)

			pending_order[self.order_id] = self.total_price
			total_sum += self.total_price
			orders_amount += self.amount

			self.cache.set(self.coin, [pending_order, total_sum, orders_amount])

			self.check_pending_order()

		else:
			self.cache.set(self.coin, [{str(self.order_id): self.total_price}, self.total_price, self.amount])

	def send_pending_order(self, orders_id, orders_amount):
		"""
			send pending order to exchange
		"""
		orders = Order.objects.filter(pk__in=orders_id)

		# i assume call buy_from_exchange always is success,
		# so i didn't check if buying from exchange is success to update order in db
		ExchangeHandler.buy_from_exchange(self.coin, orders_amount)

		orders.update(status=OrderStatus.success)

		self.cache.remove(self.coin)

	def check_pending_order(self):
		"""
			check pending order that cached in redis and check if sum of them is upper than exchange limit
		"""

		pending_order, total_sum, orders_amount = self.cache.get(self.coin)

		if total_sum >= ORDER_LIMIT:
			self.send_pending_order(orders_id=[i for i in pending_order.keys()], orders_amount=orders_amount)
