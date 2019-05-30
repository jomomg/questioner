from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.response import success_, error_


class ListViewBase(APIView):
    serializer_class = None
    model = None

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            resp = success_(f'{self.model.__name__} created', data=serializer.data)
            return Response(resp, status=status.HTTP_201_CREATED)
        return Response(error_('An error occurred', serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        events = self.model.objects.all()
        serializer = self.serializer_class(events, many=True)
        response = success_(f'Retrieved all {self.model.__name__.lower()}s', data=serializer.data)
        return Response(response, status.HTTP_200_OK)


class DetailViewBase(APIView):
    serializer_class = None
    model = None

    def get_object(self, pk):
        """
        Helper method for retrieving saved objects and handling resultant
        exceptions
        """
        exc = False
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            exc = True
            response = error_('Not found')
            return exc, Response(response, status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            exc = True
            response = error_('An error occurred', data=err)
            return exc, Response(response, status.HTTP_400_BAD_REQUEST)
        else:
            return exc, instance

    def get(self, request, pk):
        err, ret = self.get_object(pk)
        if err:
            return ret
        serializer = self.serializer_class(ret)
        response = success_(f'{self.model.__name__} retrieved', data=serializer.data)
        return Response(response, status.HTTP_200_OK)

    def patch(self, request, pk):
        err, ret = self.get_object(pk)
        if err:
            return ret
        serializer = self.serializer_class(ret, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            resp = success_(f'{self.model.__name__} updated', data=serializer.data)
            return Response(resp, status.HTTP_200_OK)
        resp = error_('An error_ occurred', serializer.errors)
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)
