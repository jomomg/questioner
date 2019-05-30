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
        pass
