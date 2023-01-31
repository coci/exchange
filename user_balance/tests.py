from django.test import TestCase

from rest_framework.test import APIClient


class UserBalanceTestCases(TestCase):

	def setUp(self) -> None:
		self.clients = APIClient()
		self.user = self.client.post('/api/v1/user/',
		                             {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                              'first_name': 'soroush', 'last_name': 'safari', 'is_active': True},
		                             ).json()

		token = self.clients.post('/api/v1/token/', {'username': 'admin', 'password': 'QazXSwEDC!'}).json()['access']

		self.clients.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

	def test_add_balance_successfully(self):
		request = self.clients.put('/api/v1/user_balance/', {'user': self.user['id'], 'balance': 20})

		self.assertEqual(request.status_code, 200)

	def test_add_zero_balance(self):
		request = self.clients.put('/api/v1/user_balance/', {'user': self.user['id'], 'balance': 0})

		self.assertEqual(request.status_code, 200)

	def test_add_negative_balance(self):
		request = self.clients.put('/api/v1/user_balance/', {'user': self.user['id'], 'balance': -10})

		self.assertEqual(request.status_code, 400)

	def test_lack_balance(self):
		request = self.clients.put('/api/v1/user_balance/', {'user': self.user['id']})

		self.assertEqual(request.status_code, 400)
