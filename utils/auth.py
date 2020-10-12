from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from rest_framework_jwt.settings import api_settings
from main.models import SelectedSphere, Observation
from users.models import Transaction
from utils import general
import constants

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def auth_user_data(user, request):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    spheres = []
    last_transaction = Transaction.objects.filter(user=user).first()
    premium_type = None
    if last_transaction:
        premium_type = f'{last_transaction.time_amount} ' \
                       f'{general.get_type_name(constants.TIME_FRAMES, last_transaction.time_unit)}' \
                       f'{_("s") if last_transaction.time_amount > 1 else ""}'
    for sphere in SelectedSphere.objects.filter(user=user):
        spheres.append({
            'id': sphere.id,
            'sphere': sphere.sphere,
            'description': sphere.description
        })
    return {
        'token': token,
        'hasSpheres': SelectedSphere.objects.filter(user=user).count() == 3,
        'spheres': spheres,
        'email': user.email,
        'isPremium': user.is_premium,
        'premiumType': premium_type,
        'notConfirmedCount': Observation.objects.filter(Q(observer=user) & Q(is_confirmed=None)).distinct(
            'observer').count()
    }
