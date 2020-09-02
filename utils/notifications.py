import requests, constants


def send_notification(fcm_token, type):
    parameters = { 
        'notification': {
            'title': get_texts(type)[0],
            'body': get_texts(type)[1],
            'sound': 'default',
            'badge': 1
        },
        'data': {
            'type': type
        },
        'to': fcm_token
    }
    headers = {
        'Authorization': f'key={constants.FIREBASE_SERVER_KEY}'
    }
    requests.request(method='POST', url=constants.FCM_SEND_URL, json=parameters, headers=headers)


def get_texts(type):
    if type == constants.NOTIFICATION_3DAYS:
        return constants.THREE_DAYS_TITLE, constants.THREE_DAYS_BODY
    if type == constants.NOTIFICATION_BEFORE_END:
        return constants.BEFORE_END_TITLE, constants.BEFORE_END_BODY
    if type == constants.NOTIFICATION_END:
        return constants.END_TITLE, constants.END_BODY
