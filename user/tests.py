from django.test import TestCase

from rest_framework.test import APIClient


class SavedModelsTestCase(TestCase):
	clients = APIClient()

	def test_create_user_successfully(self):
		request = self.client.post('/api/v1/user/',
		                           {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                            'first_name': 'soroush', 'last_name': 'safari'}, format='json')

		self.assertEqual(request.status_code, 201)

	def test_create_user_weak_password(self):
		request = self.client.post('/api/v1/user/',
		                           {'username': 'admin', 'password': '123456', 'password2': 'QazXSwEDC!',
		                            'first_name': 'soroush', 'last_name': 'safari'}, format='json')
		self.assertEqual(request.status_code, 400)

	def test_create_user_lack_first_and_last_name(self):
		request = self.client.post('/api/v1/user/',
		                           {'username': 'admin', 'password': '123456', 'password2': 'QazXSwEDC!'},
		                           format='json')
		self.assertEqual(request.status_code, 400)

	def test_create_user_lack_password1(self):
		request = self.client.post('/api/v1/user/',
		                           {'username': 'admin', 'password2': 'QazXSwEDC!',
		                            'first_name': 'soroush', 'last_name': 'safari'}, format='json')
		self.assertEqual(request.status_code, 400)

	def test_create_user_lack_password2(self):
		request = self.client.post('/api/v1/user/', {'username': 'admin', 'password': 'QazXSwEDC!',
		                                             'first_name': 'soroush', 'last_name': 'safari'}, format='json')
		self.assertEqual(request.status_code, 400)

	def test_create_user_with_exist_username(self):
		request = self.client.post('/api/v1/user/',
		                           {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                            'first_name': 'soroush', 'last_name': 'safari'}, format='json')
		self.assertEqual(request.status_code, 201)

		request = self.client.post('/api/v1/user/',
		                           {'username': 'admin', 'password': 'QazXSwEDC!', 'password2': 'QazXSwEDC!',
		                            'first_name': 'soroush', 'last_name': 'safari'}, format='json')
		self.assertEqual(request.status_code, 400)

	def test_create_user_lack_username(self):
		request = self.client.post('/api/v1/user/', {'password': 'QazXSwEDC!',
		                                             'first_name': 'soroush', 'last_name': 'safari'}, format='json')
		self.assertEqual(request.status_code, 400)
