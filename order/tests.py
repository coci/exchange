import time

import redis
from django.test import TestCase

from rest_framework.test import APIClient

from common.env import REDIS_HOST, REDIS_PORT, REDIS_DB
from order.models import Order


class MakingOrderTestCases(TestCase):

	def setUp(self) -> None:
		self.clients = APIClient()
		self.user = self.client.post('/api/v1/user/',
		                             {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                              'first_name': 'soroush', 'last_name': 'safari', 'is_active': True},
		                             ).json()

		token = self.clients.post('/api/v1/token/', {'username': 'admin', 'password': 'QazXSwEDC!'}).json()['access']

		self.clients.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

	def test_successful_order(self):
		self.clients.put('/api/v1/user_balance/', {'user': self.user['id'], 'balance': 100})

		order = self.clients.post('/api/v1/order/', {'coin': 'ABAN', 'amount': 3})

		self.assertEqual(order.status_code, 201)

	def test_successful_order_with_success_status(self):
		self.clients.put('/api/v1/user_balance/', {'user': self.user['id'], 'balance': 100})

		order = self.clients.post('/api/v1/order/', {'coin': 'ABAN', 'amount': 3})

		self.assertEqual(order.status_code, 201)
		self.assertEqual(order.json()['status'], 'success')

	def test_successful_order_with_pending_status(self):
		self.clients.put('/api/v1/user_balance/', {'user': self.user['id'], 'balance': 100})

		order = self.clients.post('/api/v1/order/', {'coin': 'ABAN', 'amount': 1})

		self.assertEqual(order.status_code, 201)
		self.assertEqual(order.json()['status'], 'pending')

	def test_pending_order(self):
		self.clients.put('/api/v1/user_balance/', {'user': self.user['id'], 'balance': 100})

		order1 = self.clients.post('/api/v1/order/', {'coin': 'ABAN1', 'amount': 1}).json()
		order2 = self.clients.post('/api/v1/order/', {'coin': 'ABAN1', 'amount': 1}).json()
		order3 = self.clients.post('/api/v1/order/', {'coin': 'ABAN1', 'amount': 1}).json()

		order1_obj = Order.objects.get(pk=order1['id'])
		order2_obj = Order.objects.get(pk=order2['id'])
		order3_obj = Order.objects.get(pk=order3['id'])

		self.assertEqual(order1_obj.status, 'success')
		self.assertEqual(order2_obj.status, 'success')
		self.assertEqual(order3_obj.status, 'success')

		redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
		redis_connection.delete('ABAN1')
