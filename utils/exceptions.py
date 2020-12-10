from rest_framework.views import exception_handler
from django.http import Http404
from utils import response as res


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, dict) and exc.detail.get('messages'):
            custom_response_data = {
                'messages': exc.detail.get('messages')
            }
        else:
            messages = []
            try:
                for key, value in exc.detail.items():
                    if isinstance(value, dict):
                        for key2, value2 in value.items():
                            messages.append(f'{key2.capitalize()}: {value2[0]}')
                    else:
                        messages.append(f'{key.capitalize()}: {value[0]}')
                custom_response_data = res.make_messages(messages)
            except:
                custom_response_data = {
                    'messages': exc.detail
                }
        response.data = custom_response_data

    return response
