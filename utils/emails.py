from utils import encryption, deeplinks
from users.views import UserViewSet

import constants


def generate_activation_email(email):
    return f"""
    {constants.ACTIVATION_EMAIL_BODY_START}
    {deeplinks.construct_link(constants.DEEPLINK_AUTH, email=encryption.encrypt(email))}
    {constants.ACTIVATION_EMAIL_BODY_END}
    """


def generate_observation_confirmation_email(email):
    return f"""
    {constants.ACTIVATION_EMAIL_BODY_START}
    {deeplinks.construct_link(constants.DEEPLINK_PREMIUM, email=email)}
    {constants.ACTIVATION_EMAIL_BODY_END}
    """
