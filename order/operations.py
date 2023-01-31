import os

import redis
from pickle import loads, dumps

from django.db import transaction
from django.db.models import Sum

from common.env import REDIS_DB, REDIS_HOST, COIN_PRICE
from order.models import Order, OrderStatus


def buy_from_exchange(coin, amount):
	print(coin, amount)


@transaction.atomic
def check_pending_order(coin):
	redis_connection = redis.Redis(host=REDIS_HOST, db=REDIS_DB)
	pending_order, total_sum = loads(redis_connection.get(coin))

	if total_sum >= 10:
		orders = Order.objects.filter(pk__in=pending_order.keys())
		buy_from_exchange(coin, orders.aggregate((Sum('coin_amount')['coin_amount__sum'])))
		orders.update(status=OrderStatus.success)
		redis_connection.delete(coin)


def set_pending_order(order_id, coin, amount):
	redis_connection = redis.Redis(host=REDIS_HOST, db=REDIS_DB)
	total_price = amount * COIN_PRICE

	if redis_connection.get(coin):
		pending_order, total_sum = loads(redis_connection.get(coin))

		pending_order[order_id] = total_price
		total_sum += total_price

		data = dumps([{str(order_id): total_price}, total_price])
		redis_connection.set(coin, data)

		check_pending_order(coin=coin)

	else:
		data = dumps([{str(order_id): total_price}, total_price])
		redis_connection.set(coin, data)
