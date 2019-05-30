from rest_framework.views import exception_handler

from utils.response import error_


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        detail = response.data['detail']
        response.data = error_(detail)
    return response
