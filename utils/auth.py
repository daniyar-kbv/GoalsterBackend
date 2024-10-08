from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from dateutil.relativedelta import relativedelta
from main.models import SelectedSphere, Observation
from main.tasks import send_email
from users.models import Transaction, MainUser, Profile
from users.serializers import UserSendActivationEmailSerializer, ProfileSerializer
from push_notifications.models import PeriodicNotification, NonCustomizableNotificationType
from push_notifications.serializers import PeriodicNotificationSerializer, NonCustomizableNotificationTypeSerializer
from utils import response, emails, types, language
import constants, datetime

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def auth_user_data(user, request):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    spheres = []
    last_transaction = Transaction.objects.filter(user=user).first()
    premium_type = None
    premium_end_date = None
    if last_transaction:
        premium_type = f'{last_transaction.time_amount} ' \
                       f'{types.get_type_value(constants.TIME_FRAMES, last_transaction.time_unit)}' \
                       f'{_("s") if last_transaction.time_amount > 1 else ""}'
        premium_end_date = (
            last_transaction.created_at + (
                relativedelta(months=last_transaction.time_amount)
                if last_transaction.time_unit == constants.MONTH else
                relativedelta(years=last_transaction.time_amount)
            )
        ).strftime(constants.DATE_FORMAT)
    for sphere in SelectedSphere.objects.filter(user=user):
        spheres.append({
            'id': sphere.id,
            'sphere': sphere.sphere,
            'description': sphere.description
        })
    profile_data = ProfileSerializer(
        user.profile,
        context={
            'request': request
        }).data \
        if Profile.objects.filter(user=user).exists() \
        else None
    periodic_notifications = PeriodicNotification.objects.all()
    periodic_notifications_data = PeriodicNotificationSerializer(periodic_notifications, many=True).data
    non_customizable_notifications = NonCustomizableNotificationType.objects.filter(
        type__in=[constants.NOTIFICATION_3DAYS, constants.NOTIFICATION_COMPLETE_GOALS]
    )
    non_customizable_notifications_data = NonCustomizableNotificationTypeSerializer(non_customizable_notifications,
                                                                                    many=True).data
    return {
        'token': token,
        'hasSpheres': SelectedSphere.objects.filter(user=user).count() == 3,
        'spheres': spheres,
        'email': user.email,
        'profile': profile_data,
        'isPremium': user.is_premium,
        'premiumType': premium_type,
        'premiumEndDate': premium_end_date,
        'notConfirmedCount': Observation.objects.filter(Q(observer=user) & Q(is_confirmed=None)).distinct(
            'observer').count(),
        'showResults': user.show_results,
        'periodic_notifications': periodic_notifications_data,
        'non_customizable_notifications': non_customizable_notifications_data
    }


def send_verification_email(request, version):
    serializer = UserSendActivationEmailSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data.get('email') == constants.APPLE_TEST_EMAIL:
            try:
                user = MainUser.objects.get(email=serializer.validated_data.get('email'))
            except:
                return Response({
                    'emailed': True
                })
            return Response(auth_user_data(user, request))
        else:
            request_language = language.get_request_language(request)
            if request_language == constants.LANGUAGE_RUSSIAN:
                subject = constants.ACTIVATION_EMAIL_SUBJECT_RU
            else:
                subject = constants.ACTIVATION_EMAIL_SUBJECT_EN
            send_email.delay(subject,
                             emails.generate_activation_email(
                                 serializer.validated_data.get('email'),
                                 request_language,
                                 version
                             ),
                             serializer.validated_data.get('email'))
            return Response({
                'emailed': True
            })
    return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)
