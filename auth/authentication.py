import os
import jwt
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class JWTAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    model = User

    def authenticate_credentials(self, token):
        secret = os.getenv('SECRET_KEY')
        try:
            decoded = jwt.decode(token, secret, algorithms='HS256')
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Expired token')
        except jwt.exceptions.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        try:
            user = User.objects.get(username=decoded['username'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        else:
            return user, token
