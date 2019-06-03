from django.urls import reverse
from rest_framework.test import APITestCase

from .fixtures import REGISTRATION_DATA


class AuthenticatedBaseTestCase(APITestCase):
    def set_auth_credentials(self):
        url = reverse('register')
        self.client.post(url, data=REGISTRATION_DATA, format='json')
        url = reverse('login')
        login_data = {
            'username': REGISTRATION_DATA['username'],
            'password': REGISTRATION_DATA['password']
        }
        resp = self.client.post(url, data=login_data, format='json')
        token = resp.data['data']['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.decode()}')

    def setUp(self):
        self.set_auth_credentials()
