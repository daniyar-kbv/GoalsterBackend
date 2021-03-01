from django.template.loader import render_to_string
from utils import deeplinks, encoding
from email.mime.text import MIMEText

import constants


def generate_activation_email(email, language, version):
    if language == 'ru-ru':
        start = constants.ACTIVATION_EMAIL_BODY_START_RU
        end = constants.ACTIVATION_EMAIL_BODY_END_RU
    else:
        start = constants.ACTIVATION_EMAIL_BODY_START_EN
        end = constants.ACTIVATION_EMAIL_BODY_END_EN
    if version == 1:
        link = deeplinks.construct_link(constants.DEEPLINK_AUTH, email=encoding.encode(email))
    elif version == 2:
        link = deeplinks.construct_link_v2(constants.DEEPLINK_AUTH, email=encoding.encode(email))
    elif version == 3:
        link = deeplinks.construct_link_v3(constants.DEEPLINK_AUTH, email=encoding.encode(email))
    elif version == 4:
        link = deeplinks.construct_link_v4(constants.DEEPLINK_AUTH, email=encoding.encode(email))
    return f"""{start}

{link}

{end}"""


def generate_activation_email_v2(request, language, otp):
    if language == 'ru-ru':
        email_top = constants.EMAIL_TOP_RU
        bottom_1 = constants.EMAIL_BOTTOM_1_RU
        bottom_2 = constants.EMAIL_BOTTOM_2_RU
        body_1 = constants.EMAIL_CODE_BODY_RU
        body_2 = constants.EMAIL_CODE_BODY_2_RU
    else:
        email_top = constants.EMAIL_TOP_EN
        bottom_1 = constants.EMAIL_BOTTOM_1_EN
        bottom_2 = constants.EMAIL_BOTTOM_2_EN
        body_1 = constants.EMAIL_CODE_BODY_EN
        body_2 = constants.EMAIL_CODE_BODY_2_EN
    base_url = '/'.join(request.build_absolute_uri().split('/')[0:3])
    context = {
        'email_top': email_top,
        'bottom_1': bottom_1,
        'bottom_2': bottom_2,
        'body_1': body_1,
        'body_2': body_2,
        'code': otp,
        'base_url': base_url
    }
    return render_to_string('code.html', context)


def generate_premium_email(language):
    if language == 'ru-ru':
        body = constants.PREMIUM_EMAIL_BODY_RU
    else:
        body = constants.PREMIUM_EMAIL_BODY_EN
    return f"""{body}
"""


def generate_premium_email_v2(request, language):
    if language == 'ru-ru':
        email_top = constants.EMAIL_TOP_RU
        bottom_1 = constants.EMAIL_BOTTOM_1_RU
        bottom_2 = constants.EMAIL_BOTTOM_2_RU
        body_1 = constants.EMAIL_PURCHASE_BODY_1_RU
        body_2 = constants.EMAIL_PURCHASE_BODY_2_RU
        body_3 = constants.EMAIL_PURCHASE_BODY_3_RU
        body_4 = constants.EMAIL_PURCHASE_BODY_4_RU
        body_5 = constants.EMAIL_PURCHASE_BODY_5_RU
        link = constants.EMAIL_PURCHASE_LINK_RU
    else:
        email_top = constants.EMAIL_TOP_EN
        bottom_1 = constants.EMAIL_BOTTOM_1_EN
        bottom_2 = constants.EMAIL_BOTTOM_2_EN
        body_1 = constants.EMAIL_PURCHASE_BODY_1_EN
        body_2 = constants.EMAIL_PURCHASE_BODY_2_EN
        body_3 = constants.EMAIL_PURCHASE_BODY_3_EN
        body_4 = constants.EMAIL_PURCHASE_BODY_4_EN
        body_5 = constants.EMAIL_PURCHASE_BODY_5_EN
        link = constants.EMAIL_PURCHASE_LINK_EN
    base_url = '/'.join(request.build_absolute_uri().split('/')[0:3])
    context = {
        'email_top': email_top,
        'bottom_1': bottom_1,
        'bottom_2': bottom_2,
        'body_1': body_1,
        'body_2': body_2,
        'body_3': body_3,
        'body_4': body_4,
        'body_5': body_5,
        'link': link,
        'base_url': base_url
    }
    return render_to_string('purchase.html', context)


def generate_observation_confirmation_email(email, language, version):
    if language == 'ru-ru':
        start = constants.OBSERVATION_EMAIL_BODY_START_RU
        end = constants.OBSERVATION_EMAIL_BODY_END_RU
    else:
        start = constants.OBSERVATION_EMAIL_BODY_START_EN
        end = constants.OBSERVATION_EMAIL_BODY_END_EN
    if version == 1:
        link = deeplinks.construct_link(constants.DEEPLINK_PREMIUM, email=encoding.encode(email))
    elif version == 2:
        link = deeplinks.construct_link_v2(constants.DEEPLINK_PREMIUM, email=encoding.encode(email))
    elif version == 3:
        link = deeplinks.construct_link_v3(constants.DEEPLINK_PREMIUM, email=encoding.encode(email))
    elif version == 4:
        link = deeplinks.construct_link_v4(constants.DEEPLINK_PREMIUM, email=encoding.encode(email))
    return f"""{start}
    
{link}
    
{end}"""


def generate_observation_confirmation_email_v2(request, language):
    if language == 'ru-ru':
        email_top = constants.EMAIL_TOP_RU
        bottom_1 = constants.EMAIL_BOTTOM_1_RU
        bottom_2 = constants.EMAIL_BOTTOM_2_RU
        body_1 = constants.EMAIL_MENTOR_BODY_1_RU
        body_2 = constants.EMAIL_MENTOR_BODY_2_RU
    else:
        email_top = constants.EMAIL_TOP_EN
        bottom_1 = constants.EMAIL_BOTTOM_1_EN
        bottom_2 = constants.EMAIL_BOTTOM_2_EN
        body_1 = constants.EMAIL_MENTOR_BODY_1_EN
        body_2 = constants.EMAIL_MENTOR_BODY_2_EN
    base_url = '/'.join(request.build_absolute_uri().split('/')[0:3])
    context = {
        'email_top': email_top,
        'bottom_1': bottom_1,
        'bottom_2': bottom_2,
        'body_1': body_1,
        'body_2': body_2,
        'base_url': base_url
    }
    return render_to_string('mentor.html', context)