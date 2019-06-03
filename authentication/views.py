import os
import jwt

from rest_framework.authentication import authenticate
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.serializers import UserSerializer
from utils.response import success_, error_


class Register(APIView):
    permission_classes = []

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp = success_('successfully registered', data=serializer.data)
            return Response(resp, status.HTTP_201_CREATED)
        resp = error_('An error occurred', data=serializer.errors)
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = []

    def post(self, request):
        login_credentials = self.validate_login_data(request.data)
        user = authenticate(**login_credentials)
        if not user:
            return Response(error_('invalid login credentials'), status.HTTP_401_UNAUTHORIZED)
        else:
            payload = {
                'username': user.username,
                'email': user.email,
                'is_staff': False
            }
            secret = os.getenv('SECRET_KEY')
            token = jwt.encode(payload, secret, algorithm='HS256')
            return Response(success_('login successful', {'token': token}), status.HTTP_200_OK)

    @staticmethod
    def validate_login_data(request_data):
        if not request_data:
            raise exceptions.ParseError('you must provide login credentials')
        required_fields = ('username', 'password')
        for field in required_fields:
            if field not in request_data:
                raise exceptions.ParseError(f'{field} is required')
            if not request_data[field]:
                raise exceptions.ParseError(f'{field} cannot be left blank')
        return request_data
