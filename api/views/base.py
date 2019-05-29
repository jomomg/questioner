from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.response import wrap_response


class ListViewBase(APIView):
    serializer_class = None
    model = None

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                wrap_response(f'{self.model.__name__} created',
                              data=serializer.data),
                status=status.HTTP_201_CREATED)
        return Response(wrap_response('An error occurred',
                                      serializer.errors, error=True),
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        events = self.model.objects.all()
        serializer = self.serializer_class(events, many=True)
        response = wrap_response(
            f'Retrieved all {self.model.__name__.lower()}s',
            data=serializer.data)
        return Response(response, status.HTTP_200_OK)


class DetailViewBase(APIView):
    serializer_class = None
    model = None

    def get_object(self, pk):
        """
        Helper method for retrieving saved objects and handling resultant
        exceptions
        """
        error = False
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            error = True
            response = wrap_response('Not found', error=True)
            return error, Response(response, status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            error = True
            response = wrap_response('An error occurred', data=err, error=True)
            return error, Response(response, status.HTTP_400_BAD_REQUEST)
        else:
            return error, instance

    def get(self, request, pk):
        error, ret = self.get_object(pk)
        if error:
            return ret
        serializer = self.serializer_class(ret)
        response = wrap_response(f'{self.model.__name__} retrieved',
                                 data=serializer.data)
        return Response(response, status.HTTP_200_OK)

    def patch(self, request, pk):
        error, ret = self.get_object(pk)
        if error:
            return ret
        serializer = self.serializer_class(ret, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            resp = wrap_response(f'{self.model.__name__} updated', data=serializer.data)
            return Response(resp, status.HTTP_200_OK)
        resp = wrap_response('An error occurred', serializer.errors, error=True)
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)
