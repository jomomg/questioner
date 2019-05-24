def wrap_response(message, data=None, error=False):
    response = {
        'status': 'success',
        'message': message,
        'data': data
    }
    if error:
        response['status'] = 'error'
        response['message'] = message
        if data:
            response['errors'] = data
        response.pop('data')
    return response
