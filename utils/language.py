import constants


def get_request_language(request) -> int:
    header = request.headers.get('Accept-Language')
    if header == 'ru-ru':
        return constants.LANGUAGE_RUSSIAN
    return constants.LANGUAGE_ENGLISH