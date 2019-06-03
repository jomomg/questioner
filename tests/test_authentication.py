from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .fixtures import REGISTRATION_DATA


class AuthenticationTestCase(APITestCase):
    def test_registration_succeeds(self):
        url = reverse('register')
        response = self.client.post(url, data=REGISTRATION_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_data = response.data['data']
        self.assertEqual(resp_data['username'], REGISTRATION_DATA['username'])
        self.assertEqual(resp_data['email'], REGISTRATION_DATA['email'])

    def test_registration_with_insufficient_credentials_fails(self):
        registration_data = {'username': 'test_user'}
        url = reverse('register')
        response = self.client.post(url, data=registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')

    def test_registration_with_duplicate_credentials_fails(self):
        url = reverse('register')
        self.client.post(url, data=REGISTRATION_DATA, format='json')
        response = self.client.post(url, data=REGISTRATION_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')

    def test_login_succeeds(self):
        url = reverse('login')
        login_data = {
            'username': REGISTRATION_DATA['username'],
            'password': REGISTRATION_DATA['password']
        }
        self.client.post(reverse('register'), data=REGISTRATION_DATA, format='json')
        response = self.client.post(url, data=login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['data']['token'])

    def test_login_without_credentials_fails(self):
        url = reverse('login')
        login_data = {}
        self.client.post(reverse('register'), data=REGISTRATION_DATA, format='json')
        response = self.client.post(url, data=login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'you must provide login credentials')

    def test_login_with_insufficient_credentials_fails(self):
        url = reverse('login')
        login_data = {'username': REGISTRATION_DATA['username']}
        self.client.post(reverse('register'), data=REGISTRATION_DATA, format='json')
        response = self.client.post(url, data=login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'password is required')

    def test_login_with_blank_credentials_fails(self):
        url = reverse('login')
        login_data = {'username': REGISTRATION_DATA['username'], 'password': ""}
        self.client.post(reverse('register'), data=REGISTRATION_DATA, format='json')
        response = self.client.post(url, data=login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'password cannot be left blank')

    def test_login_with_incorrect_credentials_fails(self):
        url = reverse('login')
        login_data = {
            'username': REGISTRATION_DATA['username'],
            'password': 'wrong_password'
        }
        self.client.post(reverse('register'), data=REGISTRATION_DATA, format='json')
        response = self.client.post(url, data=login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data['message'], 'invalid login credentials')
