import os

import redis
from pickle import loads, dumps

from django.db import transaction
from django.db.models import Sum

from common.env import REDIS_DB, REDIS_HOST, COIN_PRICE, ORDER_LIMIT
from order.models import Order, OrderStatus


def buy_from_exchange(coin, amount):
	pass


def send_pending_order(orders_id, coin, orders_amount):
	"""
		send pending order to exchange
	"""
	redis_connection = redis.Redis(host=REDIS_HOST, db=REDIS_DB)
	orders = Order.objects.filter(pk__in=orders_id)

	# i assume call buy_from_exchange always is success,
	# so i didn't check if buying from exchange is success to update order in db
	buy_from_exchange(coin, orders_amount)

	orders.update(status=OrderStatus.success)

	redis_connection.delete(coin)


def check_pending_order(coin):
	"""
		check pending order that cached in redis and check if sum of them is upper than exchange limit
	"""
	redis_connection = redis.Redis(host=REDIS_HOST, db=REDIS_DB)
	pending_order, total_sum, orders_amount = loads(redis_connection.get(coin))

	if total_sum >= ORDER_LIMIT:
		send_pending_order(orders_id=pending_order.keys(), coin=coin, orders_amount=orders_amount)


def set_pending_order(order_id, coin, amount):
	"""
		cache/store pending order in redis
		format of redis will be something like this :

		"ABAN" : [{'1':5,'2':5},10,3]

		as key i stored pair and for value i stored array which first of element are the hash map of-
		orders id with proper value ( coin amount * coin price ) and the second element are the sum of-
		all pending order in this pair and for the third element i stored coin amounts.

	"""
	redis_connection = redis.Redis(host=REDIS_HOST, db=REDIS_DB)
	total_price = amount * COIN_PRICE

	if redis_connection.get(coin):
		pending_order, total_sum, orders_amount = loads(redis_connection.get(coin))

		pending_order[order_id] = total_price
		total_sum += total_price
		orders_amount += amount

		data = dumps([pending_order, total_sum, orders_amount])
		redis_connection.set(coin, data)

		check_pending_order(coin=coin)

	else:
		data = dumps([{str(order_id): total_price}, total_price, amount])
		redis_connection.set(coin, data)
