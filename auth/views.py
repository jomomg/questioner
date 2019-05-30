import os
import jwt
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from auth.serializers import UserSerializer
from utils.response import success_, error_


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            resp = success_('Successfully registered', data=serializer.data)
            return Response(resp, status.HTTP_201_CREATED)
        resp = error_('An error occurred', data=serializer.errors)
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        serializer = UserSerializer(request.data)
        if serializer.is_valid():
            try:
                user = User(**serializer.data)
            except User.DoesNotExist:
                return Response(error_('Invalid login credentials'), status.HTTP_401_UNAUTHORIZED)
            else:
                payload = {
                    'username': user.username,
                    'email': user.email,
                    'is_staff': False
                }
                secret = os.getenv('SECRET_KEY')
                token = jwt.encode(payload, secret, algorithm='HS256')
                return Response(success_('Login successful', {'token': token}), status.HTTP_200_OK)
        return Response(error_('An error occurred', serializer.errors), status.HTTP_400_BAD_REQUEST)
