from typing import Optional, List
from push_notifications.models import NonCustomizableNotificationType
import requests, constants


def send_notification(user, type):
    texts = get_texts(type, user.language)
    parameters = {
        'notification': {
            'title': texts[0],
            'body': texts[1],
            'sound': 'default',
            'badge': 1
        },
        'data': {
            'type': type
        },
        'to': user.fcm_token
    }
    headers = {
        'Authorization': f'key={constants.FIREBASE_SERVER_KEY}'
    }
    requests.request(method='POST', url=constants.FCM_SEND_URL, json=parameters, headers=headers)


def send_user_notification(user, title, body, data):
    parameters = {
        'notification': {
            'title': title,
            'body': body,
            'sound': 'default',
            'badge': 1
        },
        'data': data,
        'to': user.fcm_token
    }
    headers = {
        'Authorization': f'key={constants.FIREBASE_SERVER_KEY}'
    }
    requests.request(method='POST', url=constants.FCM_SEND_URL, json=parameters, headers=headers)


def get_texts(type, language) -> (Optional[List[str]]):
    try:
        notification_type: NonCustomizableNotificationType = NonCustomizableNotificationType.objects.get(
            type=type
        )
    except:
        return None
    if language == constants.LANGUAGE_RUSSIAN:
        return notification_type.title_ru, notification_type.body_ru
    else:
        return notification_type.title_en, notification_type.body_en


def get_topic_text(topic, language):
    if topic == constants.FIREBASE_TOPIC_INVITE:
        if language == constants.LANGUAGE_RUSSIAN:
            return constants.TOPIC_INVITE_TEXT_RU
        elif language == constants.LANGUAGE_ENGLISH:
            return constants.TOPIC_INVITE_TEXT_EN
