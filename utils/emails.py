from utils import encryption, deeplinks
from users.views import UserViewSet

import constants


def generate_activation_email(email, language):
    if language == 'ru-ru':
        start = constants.ACTIVATION_EMAIL_BODY_START_RU
        end = constants.ACTIVATION_EMAIL_BODY_END_RU
    else:
        start = constants.ACTIVATION_EMAIL_BODY_START_EN
        end = constants.ACTIVATION_EMAIL_BODY_END_EN
    return f"""{start}

{deeplinks.construct_link(constants.DEEPLINK_AUTH, email=encryption.encrypt(email))}

{end}"""


def generate_premium_email(language):
    if language == 'ru-ru':
        body = constants.PREMIUM_EMAIL_BODY_RU
    else:
        body = constants.PREMIUM_EMAIL_BODY_EN
    return f"""{body}
"""


def generate_observation_confirmation_email(email, language):
    if language == 'ru-ru':
        start = constants.OBSERVATION_EMAIL_BODY_START_RU
        end = constants.OBSERVATION_EMAIL_BODY_END_RU
    else:
        start = constants.OBSERVATION_EMAIL_BODY_START_EN
        end = constants.OBSERVATION_EMAIL_BODY_END_EN
    return f"""{start}
    
{deeplinks.construct_link(constants.DEEPLINK_PREMIUM, email=email)}
    
{end}"""
