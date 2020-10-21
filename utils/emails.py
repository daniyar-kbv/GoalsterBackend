from utils import deeplinks, encoding

import constants


def generate_activation_email(email, language):
    if language == 'ru-ru':
        start = constants.ACTIVATION_EMAIL_BODY_START_RU
        end = constants.ACTIVATION_EMAIL_BODY_END_RU
        hint = constants.LINK_HINT_RU
    else:
        start = constants.ACTIVATION_EMAIL_BODY_START_EN
        end = constants.ACTIVATION_EMAIL_BODY_END_EN
        hint = constants.LINK_HINT_EN
    return f"""{start}

{deeplinks.construct_link(constants.DEEPLINK_AUTH, email=encoding.encode(email))}

{hint}

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
        hint = constants.LINK_HINT_RU
    else:
        start = constants.OBSERVATION_EMAIL_BODY_START_EN
        end = constants.OBSERVATION_EMAIL_BODY_END_EN
        hint = constants.LINK_HINT_EN
    return f"""{start}
    
{deeplinks.construct_link(constants.DEEPLINK_PREMIUM, email=email)}

{hint}
    
{end}"""
