import os

import redis
from pickle import loads, dumps

from django.db import transaction

from common.env import REDIS_DB, REDIS_HOST, COIN_PRICE
from order.models import Order, OrderStatus


def buy_from_exchange(coin, amount):
	pass


def set_order_success_status(orders_id):
	orders = Order.objects.filter(pk__in=orders_id).update(status=OrderStatus.success)


@transaction.atomic
def set_pending_order(order_id, coin, amount):
	redis_connection = redis.Redis(host=REDIS_HOST, db=REDIS_DB)
	total_price = amount * COIN_PRICE

	if redis_connection.hgetall(coin):
		pending_order, total_sum = loads(redis_connection.get(coin))

		if total_price + total_sum >= 10:
			pass
	else:
		data = dumps([{str(order_id): total_price}, total_price])
		redis_connection.set(coin, data)
