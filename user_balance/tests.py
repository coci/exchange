from django.test import TestCase

from rest_framework.test import APIClient


class UserBalanceTestCases(TestCase):
	clients = APIClient()

	def test_add_balance_successfully(self):
		user = self.client.post('/api/v1/user/',
		                        {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                         'first_name': 'soroush', 'last_name': 'safari', 'is_active': True},
		                        ).json()

		token = self.clients.post('/api/v1/token/', {'username': 'admin', 'password': 'QazXSwEDC!'}).json()['access']

		self.clients.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
		request = self.clients.put('/api/v1/user_balance/', {'user': user['id'], 'balance': 20})

		self.assertEqual(request.status_code, 200)

	def test_add_zero_balance(self):
		user = self.client.post('/api/v1/user/',
		                        {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                         'first_name': 'soroush', 'last_name': 'safari', 'is_active': True},
		                        ).json()

		token = self.clients.post('/api/v1/token/', {'username': 'admin', 'password': 'QazXSwEDC!'}).json()['access']

		self.clients.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
		request = self.clients.put('/api/v1/user_balance/', {'user': user['id'], 'balance': 0})

		self.assertEqual(request.status_code, 200)

	def test_add_balance_without_authentication(self):
		user = self.client.post('/api/v1/user/',
		                        {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                         'first_name': 'soroush', 'last_name': 'safari', 'is_active': True},
		                        ).json()

		request = self.clients.put('/api/v1/user_balance/', {'user': user['id'], 'balance': 20})

		self.assertEqual(request.status_code, 401)

	def test_add_negative_balance(self):
		user = self.client.post('/api/v1/user/',
		                        {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                         'first_name': 'soroush', 'last_name': 'safari', 'is_active': True},
		                        ).json()

		token = self.clients.post('/api/v1/token/', {'username': 'admin', 'password': 'QazXSwEDC!'}).json()['access']

		self.clients.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
		request = self.clients.put('/api/v1/user_balance/', {'user': user['id'], 'balance': -10})

		self.assertEqual(request.status_code, 400)

	def test_lack_balance(self):
		user = self.client.post('/api/v1/user/',
		                        {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                         'first_name': 'soroush', 'last_name': 'safari', 'is_active': True},
		                        ).json()

		token = self.clients.post('/api/v1/token/', {'username': 'admin', 'password': 'QazXSwEDC!'}).json()['access']

		self.clients.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
		request = self.clients.put('/api/v1/user_balance/', {'user': user['id']})

		self.assertEqual(request.status_code, 400)
